import subprocess
import time

import requests
from invoke import task


@task
def docs(c):
    """Generate documentation by capturing the example app."""
    # Start Django dev server
    server = subprocess.Popen(
        ["poetry", "run", "python", "manage.py", "runserver", "8002"],  # noqa: S607
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        # Wait for the server to start
        for _ in range(20):
            try:
                resp = requests.get("http://localhost:8002/")  # noqa: S113
                if resp.status_code == 200:
                    break
            except Exception:
                time.sleep(0.5)
        else:
            print("Django server did not start in time.")
            server.terminate()
            return

        # Run shot-scraper
        c.run("shot-scraper html http://localhost:8002/ -o docs/index.html")
    finally:
        server.terminate()
        server.wait()


@task
def prerelease(c):
    """
    Run comprehensive pre-release checks and update all required files.

    This task performs all necessary steps to prepare the repository for release:
    1. Run linting, formatting, type checking, and dependency checks via pre-commit hooks
    2. Run quality checks and tests

    Use this before running the release task to ensure everything is ready.

    Pre-commit hooks include:
    - Code formatting (Ruff)
    - Type checking (mypy)
    - Dependency analysis (deptry)
    - Poetry validation
    """
    print("🚀 Starting comprehensive pre-release checks...")
    print("=" * 60)

    # Step 1: Run comprehensive linting, type checking, and dependency analysis
    print("\n🧹 Step 1: Running comprehensive linting, type checking, and dependency analysis")
    print("🚀 Running pre-commit hooks (includes mypy and deptry)")
    c.run("poetry run pre-commit run -a")

    print("🚀 Running manual pre-commit hooks (poetry-lock, poetry-export)")
    c.run("poetry run pre-commit run --hook-stage manual -a")

    # Step 2: Check Poetry lock file consistency
    print("\n🔍 Step 2: Checking Poetry lock file consistency")
    print("🚀 Checking Poetry lock file consistency with 'pyproject.toml'")
    c.run("poetry check --lock")

    # Step 3: Run comprehensive test suite
    print("\n🧪 Step 3: Running comprehensive test suite")
    print("🚀 Running pytest with coverage")
    c.run("poetry run pytest --cov --cov-config=pyproject.toml --cov-report=html --cov-report=term --tb=no -qq")

    print("\n" + "=" * 60)
    print("✅ Pre-release checks completed successfully!")
    print("🎉 Repository is ready for release. You can now run 'invoke release' with the appropriate rule.")
    print("   Example: invoke release --rule=patch")


@task
def release(c, rule=""):
    """
    Create a new git tag and push it to the remote repository.

    This will create a new tag and push it to the remote repository, which will trigger
    a new build and deployment of the package to PyPI.

    Args:
        rule: Version bump rule (major, minor, patch, premajor, preminor, prepatch, prerelease)

    RULE        BEFORE  AFTER
    major       1.3.0   2.0.0
    minor       2.1.4   2.2.0
    patch       4.1.1   4.1.2
    premajor    1.0.2   2.0.0-alpha.0
    preminor    1.0.2   1.1.0-alpha.0
    prepatch    1.0.2   1.0.3-alpha.0
    prerelease  1.0.2   1.0.3-alpha.0

    Examples:
        invoke release --rule=patch
        invoke release --rule=minor
        invoke release --rule=major
    """
    if not rule:
        print("❌ Error: You must specify a version bump rule.")
        print("   Example: invoke release --rule=patch")
        print("\n   Available rules: major, minor, patch, premajor, preminor, prepatch, prerelease")
        return

    print(f"🚀 Creating new release with rule: {rule}")
    print("=" * 60)

    # Step 1: Bump version
    print(f"\n📦 Step 1: Bumping version using rule '{rule}'")
    c.run(f"poetry version {rule}")

    # Get the new version
    result = c.run("poetry version -s", hide=True)
    new_version = result.stdout.strip()
    print(f"✅ New version: {new_version}")

    # Step 2: Commit version bump
    print("\n💾 Step 2: Committing version bump")
    c.run(f'git add pyproject.toml && git commit -m "Bump version to {new_version}"')

    # Step 3: Create and push tag
    print(f"\n🏷️  Step 3: Creating and pushing tag 'v{new_version}'")
    c.run(f"git tag v{new_version}")
    c.run(f"git push origin v{new_version}")
    c.run("git push")

    print("\n" + "=" * 60)
    print(f"✅ Release v{new_version} created and pushed successfully!")
    print("🎉 GitHub Actions will now build and publish the package to PyPI.")

#!/usr/bin/env python3
"""
Quick sanity check - verify backend setup without running full app
Run: python tests/test_sanity.py
"""

import sys
import subprocess
import json
from pathlib import Path

# Color codes for terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check(name, condition, error_msg=""):
    """Print check result"""
    if condition:
        print(f"{GREEN}✓{RESET} {name}")
        return True
    else:
        print(f"{RED}✗{RESET} {name}")
        if error_msg:
            print(f"  └─ {error_msg}")
        return False

def run_cmd(cmd, capture=False):
    """Run command and return result"""
    try:
        if capture:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0, result.stdout + result.stderr
        else:
            result = subprocess.run(cmd, shell=True)
            return result.returncode == 0, ""
    except Exception as e:
        return False, str(e)

def main():
    print(f"\n{YELLOW}🧪 Content Repurposer - Sanity Check{RESET}\n")

    passed = 0
    failed = 0

    # 1. Check Python
    print(f"{YELLOW}1. Python Setup{RESET}")
    ok, out = run_cmd("python --version", capture=True)
    if check("  Python installed", ok, out):
        passed += 1
    else:
        failed += 1

    # 2. Check Python packages
    print(f"\n{YELLOW}2. Backend Dependencies{RESET}")
    packages = ['flask', 'flask_cors', 'dotenv']
    for pkg in packages:
        ok, out = run_cmd(f"python -c 'import {pkg}'", capture=True)
        if check(f"  {pkg} installed", ok):
            passed += 1
        else:
            failed += 1
            print(f"    ℹ️  Run: pip install {pkg}")

    # 3. Check FFmpeg
    print(f"\n{YELLOW}3. Video Processing{RESET}")
    ok, out = run_cmd("ffmpeg -version", capture=True)
    if check("  FFmpeg installed", ok):
        passed += 1
    else:
        failed += 1
        print(f"    ℹ️  Required for video conversion")
        print(f"    ℹ️  Mac: brew install ffmpeg")
        print(f"    ℹ️  Ubuntu: sudo apt install ffmpeg")

    # 4. Check Node
    print(f"\n{YELLOW}4. Frontend Setup{RESET}")
    ok, out = run_cmd("node --version", capture=True)
    if check("  Node.js installed", ok):
        passed += 1
    else:
        failed += 1
        print(f"    ℹ️  Required for React frontend")

    # 5. Check npm packages
    print(f"\n{YELLOW}5. Frontend Dependencies{RESET}")
    frontend_path = Path(__file__).parent.parent / "frontend"
    packages_json = frontend_path / "package.json"

    if packages_json.exists():
        ok = check("  package.json found", True)
        passed += 1
    else:
        ok = check("  package.json found", False, "Missing frontend config")
        failed += 1

    ok, out = run_cmd("npm --version", capture=True)
    if check("  npm installed", ok):
        passed += 1
    else:
        failed += 1

    # 6. Check Docker (optional)
    print(f"\n{YELLOW}6. Docker (Optional){RESET}")
    ok, out = run_cmd("docker --version", capture=True)
    check("  Docker installed", ok, "(optional - for containerized dev)")

    # 7. Check env file
    print(f"\n{YELLOW}7. Configuration{RESET}")
    env_example = Path(__file__).parent.parent / ".env.example"
    if env_example.exists():
        check("  .env.example found", True)
        passed += 1
    else:
        check("  .env.example found", False)
        failed += 1

    # 8. Check project structure
    print(f"\n{YELLOW}8. Project Structure{RESET}")
    required_dirs = [
        Path(__file__).parent.parent / "backend",
        Path(__file__).parent.parent / "frontend",
        Path(__file__).parent.parent / "backend" / "utils"
    ]

    for d in required_dirs:
        check(f"  {d.name}/ exists", d.exists())
        if d.exists():
            passed += 1
        else:
            failed += 1

    # Summary
    print(f"\n{YELLOW}{'='*50}{RESET}")
    print(f"Results: {GREEN}{passed} passed{RESET}, {RED}{failed} failed{RESET}\n")

    if failed == 0:
        print(f"{GREEN}✓ All checks passed! Ready to develop.{RESET}\n")
        print(f"Next steps:")
        print(f"  1. {YELLOW}Local development:{RESET}")
        print(f"     cd projects/content-repurposer")
        print(f"     make setup  # Install Python + Node deps")
        print(f"     make dev    # Run backend + frontend")
        print(f"\n  2. {YELLOW}Docker:{RESET}")
        print(f"     docker-compose up")
        print(f"\n  3. {YELLOW}GitHub Codespaces:{RESET}")
        print(f"     https://github.com/m2ks79/content-repurposer/codespaces")
        return 0
    else:
        print(f"{RED}✗ Some checks failed. Fix errors above then retry.{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())

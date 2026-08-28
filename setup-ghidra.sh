#!/usr/bin/env bash
#
# setup-ghidra.sh : install the heavy prerequisite, Ghidra and the Java it runs on.
#
#     bash setup-ghidra.sh
#
# Run this AFTER setup.sh, and only when the book tells you it is time. You do not
# need Ghidra for the first several missions, and you learn more without it.
#
# It does two things:
#   1. installs a Java 21 runtime (Ghidra will not start without it)
#   2. downloads the latest Ghidra release and unpacks it into your home folder
#
# Ghidra is about 400 MB. That is exactly the kind of thing you never commit to
# git. The repo carries this script; the script fetches the tool. That is the
# normal, professional way to handle a big third-party dependency.

set -e

echo
echo "  == The Dragon's Eye : installing Ghidra and its Java =="
echo

if ! command -v apt >/dev/null 2>&1; then
  echo "  Need apt (the Chromebook Linux environment has it). Stopping."
  exit 1
fi

# ---- 1. Java 21 -------------------------------------------------------------
echo "  Step 1 of 2 : a Java 21 runtime."
echo
sudo apt update

if apt-cache show openjdk-21-jdk >/dev/null 2>&1; then
  # Available directly. This is the Ubuntu case, and newer Debian.
  sudo apt install -y openjdk-21-jdk
else
  # Debian bookworm (which is what the Chromebook runs) keeps JDK 21 in backports.
  # shellcheck disable=SC1091
  . /etc/os-release 2>/dev/null || true
  code="${VERSION_CODENAME:-bookworm}"
  echo "  openjdk-21 is not in the default repos. Adding ${code}-backports."
  echo "deb http://deb.debian.org/debian ${code}-backports main" \
    | sudo tee /etc/apt/sources.list.d/backports.list >/dev/null
  sudo apt update
  sudo apt install -y -t "${code}-backports" openjdk-21-jdk
fi

echo
echo "  Java check:"
java -version || { echo "  Java did not install. See the book, Part Zero."; exit 1; }

# ---- 2. Ghidra --------------------------------------------------------------
echo
echo "  Step 2 of 2 : Ghidra itself. About 400 MB, so give it a minute."
echo

DEST="$HOME/ghidra"
mkdir -p "$DEST"

# Ask GitHub for the latest release, so this script never rots to an old version.
url="$(curl -fsSL https://api.github.com/repos/NationalSecurityAgency/ghidra/releases/latest \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); z=[a["browser_download_url"] for a in d["assets"] if a["name"].endswith(".zip")]; print(z[0] if z else "")' \
  2>/dev/null || true)"

if [ -z "$url" ]; then
  echo "  Could not reach the Ghidra release list (no network, or GitHub is blocked"
  echo "  on this machine). That is fine: the book, Part Zero, has the manual"
  echo "  download steps. Do those instead."
  exit 1
fi

echo "  Downloading:"
echo "    $url"
zip="$DEST/ghidra.zip"
curl -fSL "$url" -o "$zip"

echo "  Unpacking..."
unzip -q -o "$zip" -d "$DEST"
rm -f "$zip"

dir="$(find "$DEST" -maxdepth 1 -type d -name 'ghidra_*' | sort | tail -1)"
echo
echo "  Done. Ghidra is in:"
echo "    $dir"
echo
echo "  Launch it with:"
echo "    $dir/ghidraRun"
echo
echo "  The first launch is slow while it sets itself up. That is Ghidra, not you."
echo

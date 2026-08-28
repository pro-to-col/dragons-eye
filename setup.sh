#!/usr/bin/env bash
#
# setup.sh : provision the lab. Run this on the Linux side of the Chromebook.
#
#     bash setup.sh
#
# It installs the base tools every mission needs, then checks that each one
# actually answered. It is safe to run twice: it only installs what is missing.
# It does NOT install Ghidra. That one is heavier and has its own chapter in the
# book (Part Zero).

set -e

KIT="build-essential gdb binutils file xxd ltrace strace python3 unzip wget curl less git"

echo
echo "  == The Dragon's Eye : provisioning the lab =="
echo

# The Chromebook Linux environment is Debian, which uses apt. If we are somewhere
# without apt, we cannot install for you, so we say so plainly and stop.
if ! command -v apt >/dev/null 2>&1; then
  echo "  This installer speaks apt (Debian / Ubuntu, which is what the Chromebook"
  echo "  Linux environment runs). This machine does not have apt."
  echo
  echo "  Install these with your own package manager, then run me again to check:"
  echo "    $KIT"
  echo
  exit 1
fi

echo "  Installing the base kit. You will be asked for your password."
echo "  (The screen shows nothing while you type it. That is normal, not broken.)"
echo
sudo apt update
sudo apt install -y $KIT

echo
echo "  == checking the kit =="
missing=0
for t in gcc gdb objdump strings xxd ltrace strace python3 git; do
  if command -v "$t" >/dev/null 2>&1; then
    printf "   ok    %s\n" "$t"
  else
    printf "   MISS  %s\n" "$t"
    missing=1
  fi
done

arch="$(uname -m)"
[ "$arch" = "aarch64" ] && arch="arm64"

echo
if [ "$missing" -eq 0 ]; then
  echo "  Lab is provisioned. Every tool answered."
  echo "  Ghidra is the one big thing left. When the book says it is time, run:"
  echo "    bash setup-ghidra.sh"
  echo "  You do not need it for the first several missions."
  echo
  echo "  Next: knock on the first door."
  echo "    ./missions/$arch/m01_helloghost"
else
  echo "  Something did not install. Run me again, or read the MISS lines above."
  exit 1
fi
echo

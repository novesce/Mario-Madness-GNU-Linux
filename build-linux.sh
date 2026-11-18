#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"

if [[ $(uname -sm) != "Linux x86_64" ]]; then
    echo "This build uses the x86-64 Linux Lime and LuaJIT libraries." >&2
    exit 1
fi
for tool in curl git g++ tar sha256sum pkg-config flock; do
    command -v "$tool" >/dev/null || { echo "Missing build tool: $tool" >&2; exit 1; }
done
if ! pkg-config --exists 'libvlc >= 3' 'libvlc < 4'; then
    echo "Install the VLC 3 development files (libvlc-dev on Debian/Ubuntu or libvlc on Arch)." >&2
    exit 1
fi

toolchain="$PWD/export/linux-tools"
mkdir -p "$toolchain/lib"
exec 9<"$toolchain"
flock 9

install_tool() (
    local name=$1 url=$2 checksum=$3
    [[ -x "$toolchain/$name/$name" ]] && return
    local staging
    staging=$(mktemp -d "$toolchain/$name.XXXXXX")
    trap 'rm -rf -- "$staging"' EXIT
    curl --fail --location --retry 3 "$url" -o "$staging/archive.tar.gz"
    (cd "$staging" && echo "$checksum  archive.tar.gz" | sha256sum --check)
    mkdir "$staging/dist"
    tar -xzf "$staging/archive.tar.gz" -C "$staging/dist" --strip-components=1
    mv "$staging/dist" "$toolchain/$name"
)

install_tool haxe https://github.com/HaxeFoundation/haxe/releases/download/4.2.5/haxe-4.2.5-linux64.tar.gz \
    8670bf2f2950380c62450990f8a1b3a0fff9b27653c8f31f7cb7fbcae24c1b70
install_tool neko https://github.com/HaxeFoundation/neko/releases/download/v2-3-0/neko-2.3.0-linux64.tar.gz \
    26dda28d0a51407f26218ba9c2c355c8eb23cf2b0b617274b00e4b9170fe69eb

export PATH="$toolchain/haxe:$toolchain/neko:$PATH"
export HAXE_STD_PATH="$toolchain/haxe/std" HAXELIB_PATH="$toolchain/lib" NEKOPATH="$toolchain/neko"
export LD_LIBRARY_PATH="$NEKOPATH${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

installed=$(haxelib list)
for library in hxcpp:4.3.2 lime:8.0.2 openfl:9.2.0 flixel:5.3.1 flixel-addons:3.1.1 \
               flixel-ui:2.5.0 hscript:2.5.0 hxCodec:2.6.1 linc_luajit:0.0.7; do
    name=${library%:*}
    version=${library#*:}
    if [[ "$installed" != *"$name: [$version]"* ]]; then
        haxelib install "$name" "$version" --always --quiet --skip-dependencies
        haxelib set "$name" "$version"
    fi
done

# The registry archive omits Discord RPC's native sources. The Git checkout includes its submodules.
discord_rev=2d83fa863ef0c1eace5f1cf67c3ac315d1a3a8a5
if [[ $(git -C "$HAXELIB_PATH/discord_rpc/git" rev-parse HEAD 2>/dev/null || true) != "$discord_rev" ]]; then
    haxelib git discord_rpc https://github.com/Aidan63/linc_discord-rpc.git "$discord_rev" --always --skip-dependencies
fi

haxelib run lime build linux
echo "Play with ./export/release/linux/bin/Mario"

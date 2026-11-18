# Friday Night Funkin': Mario's Madness

## Playing on Linux

For a fresh clone, follow **Building from source** below. Once built, launch the x86-64 game from the project directory.

```sh
./export/release/linux/bin/Mario
```

Keep the entire `bin` directory together if you move the game. It contains the executable, the engine's native library, the songs, and the cutscenes. The game uses OpenGL for rendering and VLC 3 for video playback. Haxe is only needed at build time.

### Building from source

On CachyOS or Arch, install the compiler and VLC packages.

```sh
sudo pacman -S --needed base-devel git curl libvlc vlc-plugin-ffmpeg
```

On Debian 13, install the corresponding build tools and VLC packages.

```sh
sudo apt install build-essential git curl pkg-config libvlc-dev vlc-plugin-base
```

Build and launch the game from the project directory.

```sh
./build-linux.sh
./export/release/linux/bin/Mario
```

The first build downloads the pinned Haxe, Neko, and engine dependencies into `export/linux-tools`. Build on the target distribution to use its C and C++ runtimes. Close the game before rebuilding because Lime rewrites the native library beside the executable.

### Paranoia's desktop effects

**Options → Mario Options → Enable Mr Virtual Mechanics** controls Paranoia's moving window and temporary wallpaper. The Linux build uses X11, including Xwayland on a Wayland desktop. During the “TOO LATE” section, the game shows the artwork behind the characters.

On GNOME, the same section changes the actual desktop wallpaper. After about 28 seconds, or if you leave the song early, the game restores your light and dark wallpapers. If you pick another wallpaper during the effect, it keeps your choice. Other desktops show the artwork inside the game.

The GNOME effect uses Python 3 and PyGObject. The package is `python-gobject` on CachyOS and Arch, or `python3-gi` on Debian.

## Psych Engine

Engine originally used on [Mind Games Mod](https://gamebanana.com/mods/301107), intended to be a fix for the vanilla version's many issues while keeping the casual play aspect of it. Also aiming to be an easier alternative to newbie coders.

## Installation:
Follow a Friday Night Funkin' source code compilation tutorial, after this you will need to install LuaJIT.

You can do this with: `haxelib install linc_luajit` on a Command prompt/PowerShell

...Or if you don't want your mod to be able to run .lua scripts, delete the "LUA_ALLOWED" line on Project.xml

## Credits:
* Shadow Mario - Coding
* RiverOaken - Arts and Animations

### Special Thanks
* Keoiki - Note Splash Animations

WARNING: This engine is still very early in development! You can request new features though
_____________________________________

# Features

## Attractive animated dialogue boxes:

![](https://user-images.githubusercontent.com/44785097/127706669-71cd5cdb-5c2a-4ecc-871b-98a276ae8070.gif)


## Atleast one change to every week:
### Week 1:
  * New Dad Left sing sprite 
  * Unused stage lights are now used
### Week 2:
  * Both BF and Skid & Pump does "Hey!" animations
  * Thunders does a quick light flash and zooms the camera in slightly
  * Added a quick transition/cutscene to Monster
### Week 3:
  * BF does "Hey!" during Philly Nice
  * Blammed has a cool new colors flash during that sick part of the song
### Week 4:
  * Better hair physics for Mom/Boyfriend (Maybe even slightly better than Week 7's :eyes:)
  * Henchmen die during all songs. Yeah :(
### Week 5:
  * Bottom Boppers and GF does "Hey!" animations during Cocoa and Eggnog
  * On Winter Horrorland, GF bops her head slower in some parts of the song.
### Week 6:
  * On Thorns, the HUD is hidden during the cutscene
  * Also there's the Background girls being spooky during the "Hey!" parts of the Instrumental

## Cool new Chart Editor changes and countless bug fixes
![](https://i.imgur.com/h6Ja7eT.png)
* You can now chart "Event" notes, which are bookmarks that trigger specific actions that usually were hardcoded on the vanilla version of the game.
* Your song's BPM can now have decimal values
* You can manually adjust a Note's strum time if you're really going for milisecond precision
* You can change a note's type on the Editor, it comes with two example types:
  * Alt Animation: Forces an alt animation to play, useful for songs like Ugh/Stress
  * Hey: Forces a "Hey" animation instead of the base Sing animation, if Boyfriend hits this note, Girlfriend will do a "Hey!" too.

## Improved Animation Debug menu (Press 8 in-game on a Debug build)
![](https://user-images.githubusercontent.com/44785097/127721062-f912853c-2513-41b8-bd66-fd80d9d4ee0f.png)
* You can now press Save Offsets to save a .txt file with the editted offsets
* You can also now change the characters while on the Menu
* Go back to the game by pressing Escape
NOTE: This should be used for fixing your character floating or being slightly under the ground! It's not for texture editting.

## Story mode menu rework:
![](https://i.imgur.com/UB2EKpV.png)
* Added a different BG to every song (less Tutorial)
* All menu characters are now in individual spritesheets, makes modding it easier.

## Credits menu
![](https://i.imgur.com/NdIQt3d.png)
* You can add a head icon, name, description and a Redirect link for when the player presses Enter while the item is currently selected.

## Awards/Achievements
* The engine comes with 16 example achievements that you can mess with and learn how it works (Check Achievements.hx and search for "checkForAchievement" on PlayState.hx)

## Options menu:
* You can change Note colors, Controls and Preferences there.
 * On Preferences you can toggle Downscroll, Anti-Aliasing, Framerate, Low Quality, Note Splashes, Hide Hud elements, Flashing Lights, etc.

## Other gameplay features:
* When the enemy hits a note, it plays the note hit animation on their strum, just like when the player hits a note.
* Lag doesn't impact the camera movement and player icon scaling anymore.
* Some stuff based on Week 7's changes has been put in (Background colors on Freeplay, Note splashes)
* You can reset your Score on Freeplay/Story Mode by pressing Reset button.
* You can listen to a song on Freeplay by pressing Space once.

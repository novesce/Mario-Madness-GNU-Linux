package;

#if linux
import sys.FileSystem;
import sys.io.Process;
import sys.thread.Thread;

class LinuxWallpaper
{
	private static var helper:Process;

	public static function apply(imagePath:String):Void
	{
		if (helper != null) return;
		var desktop = Sys.getEnv("XDG_CURRENT_DESKTOP");
		if (desktop == null) desktop = Sys.getEnv("XDG_SESSION_DESKTOP");
		if (desktop == null || desktop.toLowerCase().split(":").indexOf("gnome") < 0) return;

		try {
			var script = FileSystem.absolutePath("gnome-wallpaper.py");
			helper = new Process("python3", ["-I", script, FileSystem.absolutePath(imagePath)]);
		} catch (error:Dynamic) {
			trace('Could not start the GNOME wallpaper effect: $error');
		}
	}

	public static function restore():Void
	{
		if (helper == null) return;
		var process = helper;
		helper = null;
		// EOF also reaches the helper if the game crashes before this cleanup.
		process.stdin.close();
		Thread.create(function() {
			try {
				var message = StringTools.trim(process.stderr.readAll().toString());
				if (process.exitCode() != 0) trace('GNOME wallpaper effect: $message');
			} catch (error:Dynamic) {
				trace('Could not finish the GNOME wallpaper effect: $error');
			}
			process.close();
		});
	}
}
#end

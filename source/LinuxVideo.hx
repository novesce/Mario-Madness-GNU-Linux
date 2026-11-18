#if macro
import haxe.macro.Context;

class LinuxVideo
{
	public static function useSystemVlc():Void
	{
		// hxCodec 2.6.1 ships its Linux library symlinks as plain text files.
		// Link to the distribution's VLC 3 library and its matching decoder plugins.
		Context.onAfterTyping(function(types) {
			for (type in types) {
				switch (type) {
					case TClassDecl(ref) if (ref.get().module == "hxcodec.vlc.LibVLC" && ref.get().name == "LibVLC"):
						var metadata = ref.get().meta;
						metadata.remove(":buildXml");
						metadata.add(":buildXml", [macro "<target id='haxe'><lib name='-lvlc'/></target>"], ref.get().pos);
					default:
				}
			}
		});
	}
}
#end

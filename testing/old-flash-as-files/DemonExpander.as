package  
{
	/**
	 * ...
	 * @author LAM
	 */
	import flash.display.MovieClip;	
	import flash.display.Stage;

	import lamshell.com.CircleText;	

	import mx.core.SoundAsset;	

	import lamshell.com.ColorChange;	
	import lamshell.com.Demons;	
	import lamshell.com.GradientMaker;	
	import lamshell.com.InversionCalculation;	
	import lamshell.rads.GeigerProxy;	
	import lamshell.com.TrailEffects;	

	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.KeyboardEvent;
	import flash.events.TimerEvent;
	import flash.geom.Point;
	import flash.media.SoundTransform;
	import flash.system.fscommand;
	import flash.ui.Mouse;
	import flash.utils.Timer;
	
	public class DemonExpander extends Sprite
	{
		
		private var stageRef:Stage;
		public  var range : Number = 12;
		public  var particleCount : Number = Math.pow(range, 2);
		public  var spawnMarkLimit : Number = 3;
		private  var spawnCount : Number = 0;
		private  var spawnArray : Array;
		private  var particleArray : Array;
		
		public  var radius : Number;
		public  var expansionRate : Number = .005; 
		public  var radialExpansionRate : Number = .27;
		public  var expansionLimit : Number = 5.0;	
		public var radiusD : Number = 300;
		public var pointOfOrigin: Point;
		public var distance : Number = 10;
		public  var xOffSet : Number = 320;
		public  var yOffSet : Number = 240;
		private  var gridStart : Number;
		private  var gridEnd : Number;
		
		private  var base : Sprite;
		private var effects : TrailEffects;
		private var baseEffects : Sprite;
		private var performEffects : Boolean = true;

		
		public function DemonExpander(s:Stage)
		{
			stageRef = s;
			init();
		}
		
		/**
		 * Initializes the main sets of variables
		 *
		 */
		public function init() : void 
		{
			base = new Sprite();
			addChild(base);

			// range must be split from a  -ve half of total
			gridStart = Math.floor(range / 2);
			gridEnd = Math.ceil(range / 2);
			particleArray = new Array();
			spawnArray = new Array();
			
			pointOfOrigin = new Point();
			pointOfOrigin.x = 1000 - 100 * Math.floor(radiusD * Math.random());
			pointOfOrigin.y = 1000 - 100 * Math.floor(radiusD * Math.random());

			for (var i : uint = 0;i < range * range;i++) {
				var demon:Demon = new Demon();
				demon.takeShape("shell");
				particleArray[i] = demon;
				base.addChild(demon.manifestationHolder);
			}
			base.addEventListener(Event.ENTER_FRAME, moveGrid, false, 0, true);
			//stageRef.addEventListener(KeyboardEvent.KEY_DOWN, restartManual);
		}
		
		/**
		 * This is called every frame and expands the hyperbolic grid
		 * @param e
		 *
		 */
		private function moveGrid(e : Event) : void 
		{
			distance += expansionRate;
			radiusD += radialExpansionRate;
			
			if (distance > expansionLimit) {
				distance = 0;
				radiusD = 200;
				pointOfOrigin.x = Math.random() * radiusD;
				pointOfOrigin.y = Math.random() * radiusD;
			}
			makeGrid();
		}

		/**
		 * Sets up the initial placement of sprites
		 *
		 */
		private function makeGrid() : void 
		{
			var count : Number = 0;
			for (var i : Number = -gridStart;i < gridEnd; i++) {
				for (var ii : Number = -gridStart;ii < gridEnd; ii++) {
					var p1 : Point = new Point(i * distance * 500, ii * distance * 500);
					//var newPt : Object = InversionCalculation.calculate(pointOfOrigin, p1, radiusD);
					var newPt : Object = InversionCalculation.calculate(pointOfOrigin, p1, radiusD);
					var scale : Number = Math.abs((radiusD / newPt.scale) * .6);
					if (scale > 5) {
						scale = 5;
					}
					var demonRef:Demon = particleArray[count] as Demon;
					var spriteRef : Sprite = demonRef.manifestationHolder;
					spriteRef.scaleX = scale;
					spriteRef.scaleY = scale;
					//spriteRef.alpha 	= scale/5;
					spriteRef.x = newPt.x + xOffSet;
					spriteRef.y = newPt.y + yOffSet;
					
					var unitAngle : Number = Math.atan2(newPt.y, newPt.x);
					spriteRef.rotation = (360 * (unitAngle + Math.PI / 2) / (2 * Math.PI));
					
					if (Math.random() > .95) {
						demonRef.changeColor();
					}
					if (Math.random() > .9) {
						demonRef.changeShape("cherub");
					}
					if (Math.random() > .9) {
						demonRef.changeShape("shell");
					}
					
					count++;
				}
			}
		}

		
	}

}
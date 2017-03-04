package 
{
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


	/**
	 * This is the main class that creates the DemonCollisions app
	 *
	 * @author Luke Mrphy
	 *
	 */
	public class DemonCollisions_V2a extends Sprite
	{
		public  var range : Number = 12;
		public  var particleCount : Number = Math.pow(range, 2);
		public  var spawnMarkLimit : Number = 3;
		private  var spawnCount : Number = 0;
		private  var spawnArray : Array;
		private  var particleArray : Array;
		
		public  var radius : Number;
		public  var expansionRate : Number = .00910010; 
		public  var radialExpansionRate : Number = .8;
		public  var expansionLimit : Number = 5.0;	
		public var radiusD : Number;
		public var p0 : Point;
		public var distance : Number;
		public  var xOffSet : Number;
		public  var yOffSet : Number;
		private  var gridStart : Number;
		private  var gridEnd : Number;
		
		private  var base : Sprite;
		private var effects : TrailEffects;
		private var baseEffects : Sprite;
		private var performEffects : Boolean = true;
		private var mc : Sprite;

		private var initTimer : Timer;
		private var tmr : Timer;
		public static var started : Boolean = false;
		private var GeigerCounter : GeigerProxy;

		public var thresholdValue : Number = 9;
		public var TicIntervalAverage : Number = 1;
		public var TicIntervalTotal : Number = 1;
		public var TicIntervalSample : Number = 1;
		public var TicIntervalSampleInit : Boolean = true;
		public var timeFrame : Number = 7000;

		private var beepSound : SoundAsset;
		private var radSound : SoundAsset;
		private var s1 : SoundAsset;
		private var s2 : SoundAsset;
		private var s3 : SoundAsset;
		private var s4 : SoundAsset;
		private var s5 : SoundAsset;
		private var s6 : SoundAsset;
		private var s7 : SoundAsset;
		private var s8 : SoundAsset;

		[Embed(source="../assets/RadBlocksLib.swf", symbol="click1.wav")] 
		private var ClickSound : Class;

		[Embed(source="../assets/RadBlocksLib.swf", symbol="radiation.mp3")] 
		private var RadSound : Class;

		[Embed(source="../assets/RadBlocksLib.swf", symbol="click1.wav")] 
		private var s_1 : Class;

		[Embed(source="../assets/RadBlocksLib.swf", symbol="sound2.mp3")] 
		private var s_2 : Class;

		[Embed(source="../assets/RadBlocksLib.swf", symbol="symph1.mp3")] 
		private var s_3 : Class;

		[Embed(source="../assets/RadBlocksLib.swf", symbol="symph2.mp3")] 
		private var s_4 : Class;

		[Embed(source="../assets/RadBlocksLib.swf", symbol="symph3.mp3")] 
		private var s_5 : Class;

		[Embed(source="../assets/RadBlocksLib.swf", symbol="ahyeah.mp3")] 
		private var s_6 : Class;

		[Embed(source="../assets/RadBlocksLib.swf", symbol="blip03.mp3")] 
		private var s_7 : Class;

		[Embed(source="../assets/RadBlocksLib.swf", symbol="blip05.mp3")] 
		private var s_8 : Class;

		[Embed(source="../assets/RadBlocksLib2.swf", symbol="flare")] 
		private var flare : Class;

		private var ct : CircleText;
		
		private var stageRef:Stage;
		
		/**
		 * This initializes the application and creates 2 base sprites
		 */
		public function DemonCollisions_V2a(s:Stage)
		{
		
			stageRef = s;
			base = new Sprite();
			baseEffects = new Sprite();
			this.addChild(base);
			this.addChild(baseEffects);
			mc = GradientMaker.createGradientBitmap(600, 600, 0xffffff, "radial",100,100, false);
			base.addChild(mc);
			mc.x = -1000;
			mc.y = -1000;
			radius = 250;
			Mouse.hide();
	/*
			var test : Sprite = new Sprite();
			this.addChild(test);
			
			test.x = 300;
			test.y = 300;
			
			var demon : String = Demons.setText();
			trace('demon: ' + (demon));
			
			//ct = new CircleText(demon, 90, 270, 20, test, 0, 0);
			ct = new CircleText(demon, Math.round(Math.random() * 180), 320, 8, test, 1, 2);
			var g : MovieClip = new flare();
			test.addChild(g);
			g.addEventListener(Event.ENTER_FRAME, check);
	
			*/
			//fscommand("fullscreen", "true");
			init();
		}

		private var wd:Number = 0;
		
		private function check(e : Event) : void 
		{
			if(e.currentTarget.currentFrame == e.currentTarget.totalFrames) {
				e.currentTarget.stop();
			} else {
				
				if (e.currentTarget.width > wd) {
					wd = e.currentTarget.width
					ct.m_unitClipWordHolder.scaleX += .12;
					ct.m_unitClipWordHolder.scaleY += .12;
				} else if (e.currentTarget.width < wd) {
					ct.m_unitClipWordHolder.scaleX -= .18;
					ct.m_unitClipWordHolder.scaleY -= .18;
				}
				
				//ct.m_unitClipWordHolder.scaleX = e.currentTarget.width / 50;
				//ct.m_unitClipWordHolder.scaleY = e.currentTarget.width / 50;
			}
		}

		/**
		 * Initializes the main sets of variables
		 *
		 */
		public function init() : void 
		{

			// range must be split from a  -ve half of total
			gridStart = Math.floor(range / 2);
			gridEnd = Math.ceil(range / 2);
			particleArray = new Array();
			spawnArray = new Array();
			
			xOffSet = 320;
			yOffSet = 240;
			radiusD = 300;
			distance = 10;
			radialExpansionRate = .7;
			expansionRate = .01;
			
			p0 = new Point();
			p0.x = 1000 - 100 * Math.floor(radiusD * Math.random());
			p0.y = 1000 - 100 * Math.floor(radiusD * Math.random());
			//baseEffects.alpha = .9;

			for (var c : uint = 0;c < range * range;c++) {
				var p : Particle = new Particle();
				particleArray[c] = p;
				p.mc = mc;
				base.addChild(p.unitSprite);
			}

			TrailEffects.blurx = 10;
			TrailEffects.blury = 10;
			effects = new TrailEffects();
			effects.baseBitmapColor = 0x000000;
			effects.useEffects = true;
			effects.useColor = true;
			effects.effectClip = baseEffects;
			effects.rootClip = base;
			effects.baseBitmapColor = 0x000000;
			effects.elGreco = false;
			effects.setupEffects();

			GeigerCounter = new GeigerProxy(5332);
			GeigerCounter.demoMode = true;
			GeigerCounter.thresholdValue = thresholdValue;
			GeigerCounter.CallBack = Tick;

			initTimer = new Timer(7000);
			initTimer.addEventListener(TimerEvent.TIMER, EventFired, false, 0, true);
			initTimer.start();

			beepSound = SoundAsset(new ClickSound());
			radSound = SoundAsset(new RadSound());
			s1 = SoundAsset(new s_1());
			s2 = SoundAsset(new s_2());
			s3 = SoundAsset(new s_3());
			s4 = SoundAsset(new s_4());
			s5 = SoundAsset(new s_5());
			s6 = SoundAsset(new s_6());
			s7 = SoundAsset(new s_7());
			s8 = SoundAsset(new s_8());
			beepSound.play(0, 0, new SoundTransform(2, 0));
			s7.play(0, 0, new SoundTransform(2, 0));

			base.addEventListener(Event.ENTER_FRAME, moveGrid, false, 0, true);
			stageRef.addEventListener(KeyboardEvent.KEY_DOWN, restartManual);
		}

		/**
		 * Restarts when the "space" bar is pressed
		 * @param e
		 *
		 */
		private function restartManual(e : KeyboardEvent) : void
		{
			/*
			p0.x = 1000 - 1 * Math.floor(2000*Math.random());
			p0.y = 1000 - 1 * Math.floor(2000*Math.random());
			var n:Number = Math.floor(Math.random()*range*range);
			ColorChange.NewBaseColor(particleArray[n].unitSprite);
			 */
			if(e.charCode == 32)	restart();
		}

		/**
		 * Clears and resets
		 *
		 */
		private function restart() : void 
		{
			for (var c : uint = 0;c < range * range;c++) {
				particleArray[c].removeSpark();
			}
			distance = 0;
			radiusD = radius;
			//p0.x 		= Math.random()*radiusD;
			//p0.y 		= Math.random()*radiusD;
			p0.x = radiusD - 1 * Math.floor(radiusD * Math.random());
			p0.y = radiusD - 1 * Math.floor(radiusD * Math.random());
		}

		/**
		 * This is called back by the GeigerCounter proxy
		 * @param arg
		 *
		 */
		public function Tick(arg : Number) : void 
		{
			if (arg > thresholdValue) {
				beepSound.play();
				var chosen : Number = Math.floor(Math.random() * range * range);
				var pointRef : Particle = particleArray[chosen];

				if (pointRef.spawnCount == 5) {
					pointRef.wordSprite.scaleX = 2;
					pointRef.wordSprite.scaleY = 2;
					pointRef.markSprite.scaleX = 3;
					pointRef.markSprite.scaleY = 3;
				}

				if (pointRef.spawnCount == 0) {
					pointRef.unitSprite.scaleX *= 3;
					pointRef.unitSprite.scaleY *= 3;
				}
				
				// reverts to shell
				if (pointRef.spawnCount == 4) {
					pointRef.removeSpark();
					trace("removing");
				}

				ColorChange.NewColor(pointRef.markSprite);
				ColorChange.NewColor(pointRef.wordSprite);
			}
		}

		/**
		 * This is the timer activated - controls when the next change happens
		 * @param arg
		 *
		 */
		public function SetTimeToChangeCherubim(arg : Number) : void 
		{
			tmr = new Timer(arg, 1);
			tmr.addEventListener(TimerEvent.TIMER, EventFired, false, 0, true);
			tmr.start();
		}

		/**
		 * This is called after the SetTimeToChangeCherubim
		 * @param e
		 *
		 */
		public function EventFired(e : TimerEvent) : void 
		{
			radSound.play(0, 0, new SoundTransform(1, 0));
			if (GeigerCounter.intervalArrayShort.length >= GeigerCounter.shortSampleSize) {

				var s : Number = Math.ceil(Math.random() * 3);
				if (s == 1) {
					s8.play();
				}
				if (s == 2) {
					s8.play();
				}
				if (s == 3) {
					s8.play();
					s5.play();
				}

				var MaxValue : Number = 0;
				var MinValue : Number = 10000;

				for (var i : uint;i < GeigerCounter.shortSampleSize;i++) {
					if (GeigerCounter.intervalArrayShort[i] > MaxValue) MaxValue = GeigerCounter.intervalArrayShort[i];
					if (GeigerCounter.intervalArrayShort[i] < MinValue) MinValue = GeigerCounter.intervalArrayShort[i];
					TicIntervalTotal += Number(GeigerCounter.intervalArrayShort[i]);
				}

				TicIntervalAverage = TicIntervalTotal / GeigerCounter.shortSampleSize;
				TicIntervalSample = 0;
				TicIntervalTotal = 0;

				if (!started) {
					started = true;
					initTimer.stop();
					e.currentTarget.stop();
				}

				var ratio : Number = (GeigerCounter.intervalArrayShort[6] - MinValue) / (MaxValue - MinValue);
				//ratio =  (TicIntervalAverage - MinValue)/(MaxValue - MinValue);
				var n : Number = Math.round((range * range - 1) * ratio);
				var t : Number = Math.round(timeFrame * ratio);

				if (t < 2000) t = 2000;
				if (isNaN(n)) n = 0;

				//trace(GeigerCounter.intervalArrayShort);
				//trace(TicIntervalAverage + " " + n + " ratio = " + ratio);

				//------------------------------------------------------------//
				// Produces Spark at triggered particle
				//------------------------------------------------------------//
				if (spawnCount >= spawnMarkLimit) {
					Demons.series = Math.round(Math.random() * 7);
					spawnCount = 0;
				} else {
					setPrimary(n);
					//spawnArray[spawnCount] 		= n;
					spawnCount++;
				}

				SetTimeToChangeCherubim(t);
			}
		}

		/**
		 * This calls out the particle to invoke its change
		 * @param n
		 *
		 */
		private function setPrimary(n : Number) : void 
		{
			var particleRef : Particle = particleArray[n];
			//trace("spawn: " + n);
			particleRef.setPrimary();
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
				p0.x = Math.random() * radiusD;
				p0.y = Math.random() * radiusD;
				if(performEffects) {
					performEffects = false;
					baseEffects.addEventListener(Event.ENTER_FRAME, fader);
				}
				if (Math.random() > .9) restart();
			}
			if (performEffects) {
				baseEffects.alpha = 1;
				//effects.bm.alpha = .9;
				effects.performEffect(2, 2);
			}
			if(Math.random() > .98 && performEffects) {
				performEffects = false;
				baseEffects.addEventListener(Event.ENTER_FRAME, fader);
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
					//var newPt : Object = InversionCalculation.calculate(p0, p1, radiusD);
					var newPt : Object = InversionCalculation.calculate(p0, p1, radiusD);
					var scale : Number = Math.abs((radiusD / newPt.scale) * .6);
					if (scale > 4) {
						scale = 4;
					}
					var spriteRef : Sprite = particleArray[count].unitSprite;
					spriteRef.scaleX = scale;
					spriteRef.scaleY = scale;
					//spriteRef.alpha 	= scale/5;
					spriteRef.x = newPt.x + xOffSet;
					spriteRef.y = newPt.y + yOffSet;
					
					/*
					spriteRef.scaleX = 2;
					spriteRef.scaleY = 2;
					//spriteRef.alpha 	= scale/1.5;
					spriteRef.x = i * 150 + xOffSet + 20;
					spriteRef.y = ii * 150 + yOffSet + 20;
					*/
					
					var unitAngle : Number = Math.atan2(newPt.y, newPt.x);
					particleArray[count].markSprite.rotation = (360 * (unitAngle + Math.PI / 2) / (2 * Math.PI));;
					count++;
				}
			}
		}

		/**
		 * This fades the effects layer
		 * @param e
		 *
		 */
		private function fader(e : Event) : void 
		{
			baseEffects.alpha -= .15;
			if (baseEffects.alpha <= 0) {
				baseEffects.removeEventListener(Event.ENTER_FRAME, fader, false);
				effects.blank();
				baseEffects.alpha = 1;
				performEffects = true;
			}
		}
	}
}

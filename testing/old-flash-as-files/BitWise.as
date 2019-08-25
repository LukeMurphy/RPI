package 
{
	import flash.display.Stage;
	import flash.events.KeyboardEvent;
	import flash.filters.BlurFilter;	
	import flash.net.URLLoaderDataFormat;	
	import flash.net.URLLoader;	
	import flash.events.MouseEvent;	
	import flash.net.URLRequest;	
	import flash.display.Loader;	
	import flash.filters.ShaderFilter;	
	import flash.display.Shader;	
	import flash.net.FileReference;	
	import flash.text.TextField;	
	import flash.events.TimerEvent;	
	import flash.utils.Timer;	
	import flash.display.Bitmap;
	import flash.display.BitmapData;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.geom.Point;
	import flash.geom.Rectangle;
	import flash.utils.getTimer;

	/**
	 * @author Luke Mrphy
	 */
	public class BitWise extends Sprite 
	{
		private var fr : FileReference;  
		private var shader : Shader;  
		private var shaderFilter : ShaderFilter;  
		private var loader : Loader;  		
		private var shaderloader : URLLoader;  		
		private var hasSymmetry : Boolean = true;
		private var hasCheckers : Boolean = false;
		private var doScroll : Boolean = false;
		private var isRandom : Boolean = true;
		private var saturation : Number = .5;
		private var shift : int = 0;

		private var COLUMNS : int = 25;
		private var ROWS : int = 30;
		private var LASTROW : int = ROWS - 1;
		private var LASTCOLUMN : int = COLUMNS - 1;
		private var TILES_PER_PASS : int = Math.round(COLUMNS/5);
		
		// More radians, circle in more defined
		private var fillRads : int = 15;
		// circle radius, lower is more square
		private var fillRadius : int = 4;
		private var fillRadiusMultiplier : Number = 20;

		private const DEG_120 : Number = 120 * Math.PI / 180;
		private const DEG_240 : Number = 240 * Math.PI / 180;

		// number of tiles to draw each pass
		private var px : Number = 0;
		private var py : Number = 0;
		private var myBitmap : BitmapData;
		private var drawBitmap : BitmapData;
		private var t : Number = 0;
		private var TILE_WIDTH : Number;
		private var TILE_HEIGHT : Number;

		private var bitMapHolder : Sprite;
		private var markHolder : Sprite;
		private var textDisplay : TextField;

		private var stageRef:Stage;
		
		private var run:Boolean = true;
		
		public function BitWise(stageRef:Stage) 
		{
			this.stageRef = stageRef;
			TILE_WIDTH = stageRef.stageWidth / COLUMNS;
			TILE_HEIGHT = stageRef.stageWidth / ROWS;
			
			bitMapHolder = new Sprite();
			markHolder = new Sprite();

			addChild(bitMapHolder);
			addChild(markHolder);
			
			textDisplay = new TextField();
			textDisplay.width = 100;
			textDisplay.height = 100;
			textDisplay.background = true;
			textDisplay.backgroundColor = 0xffffff;
			
			//addChild(textDisplay);

			myBitmap = new BitmapData(COLUMNS, ROWS, false, 0x000000);
			drawBitmap = new BitmapData(stageRef.stageWidth, stageRef.stageHeight, false, 0x000000);
			var mc : Bitmap = new Bitmap(myBitmap);
			var mc2 : Bitmap = new Bitmap(drawBitmap);
			
			var fltr:Array = mc.filters;
			var bf:BlurFilter = new BlurFilter(80,100,1);
			fltr.push(bf);
			//mc.filters = fltr;


			bitMapHolder.addChild(mc2);
			bitMapHolder.addChild(mc);

			mc.scaleX = TILE_WIDTH;
			mc.scaleY = TILE_HEIGHT;
			//this.addEventListener(Event.ENTER_FRAME, drawPixels, false, 0, true);

			var tt : Timer = new Timer(500);
			tt.addEventListener(TimerEvent.TIMER, drawPixels);
			//tt.start();	

			PixelBender();
			
			
			stageRef.addEventListener(KeyboardEvent.KEY_DOWN, keyDownHandler);
		}

		private function keyDownHandler(e:KeyboardEvent):void {
			if (e.keyCode == 32) {
				if (run) trace(fillRadius + " " + fillRadiusMultiplier);
				run = (run) ? false :true;
			}
		}
		
		public function PixelBender() : void 
		{  
			shaderloader = new URLLoader(); 
			shaderloader.addEventListener(Event.COMPLETE, onComplete);
			//shaderloader.load(new URLRequest("blur_3b.pbj"));  
			shaderloader.load(new URLRequest("test-2.pbj"));  
			//shaderloader.load(new URLRequest("RippleBlocks.pbj"));  
			//shaderloader.load(new URLRequest("deformer.pbj"));  
			//shaderloader.load(new URLRequest("fisheye.pbj"));  
			shaderloader.dataFormat = URLLoaderDataFormat.BINARY;
			//addChild(shaderloader);  
			/*
			fr = new FileReference();  
			fr.addEventListener(Event.SELECT, onSelect);  
			fr.addEventListener(Event.COMPLETE, onComplete);  
			loader = new Loader();  
			loader.load(new URLRequest("lobstercreamsauce.jpg"));  
			addChild(loader);  
			loader.addEventListener(MouseEvent.CLICK, loaderClick);  
			 * 
			 */
		}  

		private function loaderClick(e : Event) : void 
		{  
			fr.browse();  
		}  

		private function onSelect(e : Event) : void 
		{  
			fr.load();  
		}  

		private function onComplete(e : Event) : void 
		{  
			//shader = new Shader(fr.data);  
			shader = new Shader(shaderloader.data);  
			shaderFilter = new ShaderFilter();  
			shaderFilter.shader = shader;  
			//loader.filters = [shaderFilter]; 
			var bf : BlurFilter = new BlurFilter(100,100,1);
			//bitMapHolder.filters = [shaderFilter];
			//markHolder.filters = [bf,bf];
			
			
			this.addEventListener(Event.ENTER_FRAME, drawPixels, false, 0, true);
		} 

		private function test() : void 
		{
			
			//t += .001;
			///if (t>255) t=0;

			var rndTint_r : Number = Math.random() * Math.PI;
			var rndTint_g : Number = Math.random() * Math.PI;
			var rndTint_b : Number = Math.random() * Math.PI;
			saturation = Math.random();
			t += .1;
			//var t : Number = getTimer() * .00051;
			var r1 : Number = 128 + Math.cos(t * Math.PI / 400 + rndTint_r * saturation) * 127;
			var g1 : Number = 128 + Math.sin(t * Math.PI / 400 + rndTint_g * saturation) * 127;
			var b1 : Number = 128 + Math.sin(t * Math.PI / 400 + rndTint_b * saturation) * 127;
			
			
			var baseStart : Number = r1;
			var baseEnd : Number = b1;
			
			var r_startValue : int = randInt(baseStart);
			var r_endValue : int = randInt(baseEnd);
			var r_step : int = Math.floor((r_endValue - r_startValue) / TILES_PER_PASS);
			
			var g_startValue : int = randInt(baseStart);
			var g_endValue : int = randInt(baseEnd);
			var g_step : int = Math.floor((g_endValue - g_startValue) / TILES_PER_PASS);
			
			var b_startValue : int = randInt(baseStart);
			var b_endValue : int = randInt(baseEnd);
			var b_step : int = Math.floor((b_endValue - b_startValue) / TILES_PER_PASS);
			
			for (var i : int = 0;i < TILES_PER_PASS; ++i) {
				py = 1;
				px = i * TILE_WIDTH / COLUMNS;
				px = Math.floor(Math.random() * COLUMNS);
				py = Math.floor(Math.random() * ROWS);
				var r : Number = r_startValue + i * r_step;
				var g : Number = g_startValue + i * g_step;
				var b : Number = b_startValue + i * b_step;
				var tint : Number = (r << 16) | (g << 8) | b;

				myBitmap.setPixel(px, py, tint);			
			}
		}

		private function randInt(arg1 : Number,arg2 : Number = 0) : int 
		{
			return arg2 + Math.floor(Math.random() * (arg1 - arg2));	
		}

		private function drawPixels(evt : Event) : void 
		{
			//test();
			drawPixelPattern();
		}

		private function drawPixelPattern__() : void 
		{
			
			/*
			var amp : Array = shader.data.amplitude.value;
			amp[0] += .1;
			amp[1] += .1;
			if(amp[0] > 100) {
			amp[0] =  amp[1] = 20;
			}
			
			shader.data.amplitude.value = amp;
			
			var sy : Array = shader.data.wavelength.value;
			sy[0] += .15;
			sy[1] += .1;
			if (sy[0] > 100) sy[0] = 0;
			if (sy[1] > 100) sy[1] = 0;
			shader.data.wavelength.value = sy;
			/*
			var sy : Number = shader.data.center_y.value;
			sy += .4;
			if (sy > 400) sy = 0;
			shader.data.center_y.value = [sy];
			
			var sx : Number = shader.data.center_x.value;
			sx += .4;
			if (sx > 400) sx = 0;
			
			shader.data.center_x.value = [sx];
			
			var ih : Number = shader.data.imageHeight.value;
			ih += .1;
			if (ih > 2000) ih = 0;
			shader.data.imageHeight.value = [ih];

			shaderFilter.shader = shader;
			bitMapHolder.filters = [shaderFilter]; 
			 */

			
			for (var i : int = 0;i < TILES_PER_PASS; ++i) {
				if (isRandom) {
					px = Math.floor(Math.random() * COLUMNS);
					py = Math.floor(Math.random() * ROWS);
				} else {
					if (++px > LASTCOLUMN) {
						px = 0;
						if (++py > LASTROW) {
							py = 0;
						}
					}
				}

				var rndTint_r : Number = Math.random() * Math.PI;
				var rndTint_g : Number = Math.random() * Math.PI;
				var rndTint_b : Number = Math.random() * Math.PI;
				saturation = Math.random();
				t += .00005;
				// * Math.PI;
				//var t : Number = getTimer() * .00051;
				var r : Number;
				var g : Number;
				var b : Number;
				if(shift == 0) {
					r = 128 + Math.cos(t + rndTint_r * saturation) * 127;
					g = 128 + Math.sin(t + rndTint_g * saturation) * 127;
					b = 128 + Math.sin(t + rndTint_b * saturation) * 127;
				} else if(shift == 1) {
					r = 128 + Math.sin(t + rndTint_r * saturation) * 127;
					g = 128 + Math.cos(t + rndTint_g * saturation) * 127;
					b = 128 + Math.sin(t + rndTint_b * saturation) * 127;
				} else if(shift == 2) {
					r = 128 + Math.sin(t + rndTint_r * saturation) * 127;
					g = 128 + Math.sin(t + rndTint_g * saturation) * 127;
					b = 128 + Math.cos(t + rndTint_b * saturation) * 127;
				} else if(shift == 3) {
					r = 128 + Math.sin(t + rndTint_r * saturation) * 127;
					g = 128 + Math.cos(t + rndTint_g * saturation) * 127;
					b = 128 + Math.cos(t + rndTint_b * saturation) * 127;
				} else if(shift == 4) {
					r = 128 + Math.cos(t + rndTint_r * saturation) * 127;
					g = 128 + Math.cos(t + rndTint_g * saturation) * 127;
					b = 128 + Math.sin(t + rndTint_b * saturation) * 127;
				}
				
				if(Math.sin(t) > .99) {
					shift++;
					//textDisplay.text = String(shift) + " \n" + String(1 / t);
				}
				
				if (shift == 5) shift = 0;

				
				var tint : Number = (r << 16) | (g << 8) | b;

				if (hasCheckers) {
					var hilo : Number = ((px + py) & 1);		
					// this produces a checkerboard pattern...
					if (hilo) {
						tint |= 0x808080;
					}	else {
						tint &= 0x7F7F7F;
					}
				}

				//myBitmap.setPixel(px, py, tint);

				/*
				 * 
				 */
				drawBitmap.draw(markHolder);
				markHolder.graphics.clear();				
				markHolder.graphics.beginFill(tint);
				//markHolder.graphics.drawCircle(px * TILE_WIDTH, py * TILE_HEIGHT, 15);				
				
				if (hasSymmetry) {
					var num : int = 8;
					var rads : Number = 2 * Math.PI / num;
					var mult : Number = 6;
					for (var ii : int = 0;ii < 8; ii++) {
						myBitmap.setPixel(px + Math.round(Math.cos(rads * ii) * TILE_WIDTH / mult), py + Math.round(Math.sin(rads * ii) * TILE_HEIGHT / mult), tint);
					}
					var tOpp : Number = tint;
					/*
					myBitmap.setPixel(LASTCOLUMN - px, py, tOpp ^= 0x111111);
					myBitmap.setPixel(LASTCOLUMN - px, py, tint);
					myBitmap.setPixel(LASTCOLUMN - px, LASTROW - py, tint);
					myBitmap.setPixel(LASTCOLUMN - px, py, tint);
					*/
					myBitmap.setPixel(px, LASTROW - py, tint);
				}
			}
			if (doScroll) {
				// scroll up via blit...
				var sourceRect : Rectangle = new Rectangle(0, 1, COLUMNS, ROWS - 1);
				var destPoint : Point = new Point(0, 0);
				myBitmap.copyPixels(myBitmap, sourceRect, destPoint);
			}
		}
	
		private function drawPixelPattern() : void 
		{
			if (run) {
				if (Math.random() > .99) {
					fillRadius = Math.random() * 6 + 1;
					//fillRads = Math.random() * ROWS + 1;
					fillRadiusMultiplier = Math.random() * ROWS + 1;
					//TILES_PER_PASS  = Math.round(Math.random() * ROWS);
					//trace(fillRadiusMultiplier);
				}
				
				for (var i : int = 0;i < TILES_PER_PASS; ++i) {
					px = Math.floor(Math.random() * COLUMNS);
					py = Math.floor(Math.random() * ROWS);

					var rndTint_r : Number = Math.random() * 0xffffff;
					var rndTint_g : Number = Math.random() * 0xffffff;
					var rndTint_b : Number = Math.random() * 0xffffff;
					saturation = Math.random();
					t += .00005;
					// * Math.PI;
					//var t : Number = getTimer() * .00051;
					var r : Number;
					var g : Number;
					var b : Number;

					var tint:int = rndTint_b;
					var rads : Number = 2 * Math.PI / fillRads;
					if (Math.random() > .5)myBitmap.setPixel(px, py, tint);
					for (var ii : int = 0;ii < fillRads; ii++) {
						myBitmap.setPixel(LASTCOLUMN - px + Math.round(Math.cos(rads * ii) * TILE_WIDTH / fillRadiusMultiplier), py + Math.round(Math.sin(rads * ii) * TILE_HEIGHT / fillRadiusMultiplier), tint);
						myBitmap.setPixel(px + Math.round(Math.cos(rads * ii) * TILE_WIDTH / fillRadiusMultiplier), LASTROW - py + Math.round(Math.sin(rads * ii) * TILE_HEIGHT / fillRadiusMultiplier), tint);
						myBitmap.setPixel(px + Math.round(Math.cos(rads * ii) * TILE_WIDTH / fillRadiusMultiplier), py + Math.round(Math.sin(rads * ii) * TILE_HEIGHT / fillRadiusMultiplier), tint);
						myBitmap.setPixel(px + Math.round(Math.cos(rads * ii) * fillRadius), py + Math.round(Math.sin(rads * ii)  * fillRadius), tint);
					}
					var arr1:Array = new Array(
					0, 1, 1, 1, 0,
					1, 1, 1, 1, 1,
					1, 0, 1, 0, 1,
					1, 1, 1, 1, 1,
					0, 1, 1, 1, 1,
					1, 0, 0, 0, 1,
					0, 1, 1, 1, 1
					);
					
					var arr2:Array = new Array(
					0, 1, 1, 1, 0,
					1, 1, 1, 1, 1,
					1, 0, 1, 0, 1,
					1, 1, 1, 1, 1,
					0, 1, 1, 1, 0,
					0, 0, 0, 0, 0,
					0, 0, 0, 0, 0
					);
					
					var arr:Array =  (Math.random() > .5) ? arr1 : arr2;
					var count:int = 0;
					for (var rw:int = 0; rw < 7; rw++) {
					for (var c:int = 0; c < 5; c++) {
							if (arr[count] == 1) myBitmap.setPixel(px + c, py + rw, tint);
							count++;
						}
					}
					
					
				}
			}
		}
	}
}

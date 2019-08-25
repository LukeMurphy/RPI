package com
{

	import flash.geom.Point;

	/**
	 * This Class manages the hyperbolic math for the grid
	 * @author Luke Mrphy
	 *
	 */
	public class InversionCalculation extends Object
	{

		public function InversionCalculation() {
		}

		/**
		 * Calculates the inversion postion -- the projection of the real point to the
		 * hyperbolic plane
		 * @param p0
		 * @param pt
		 * @param radiusD
		 * @return
		 *
		 */
		public static function calculate(p0:Point, pt:Point, radiusD:Number):Object {
			// need to return OA give OAi
			// Log((1 + X) / (1 - X)) / 2
			var dx1:Number = pt.x/2000-p0.x/radiusD;
			var dy1:Number = pt.y/2000-p0.y/radiusD;
			var dE:Number = Math.sqrt(dx1*dx1+dy1*dy1);
			if (dE == 0) {
			} else {
				var newD:Number = radiusD-radiusD*Math.log(Math.abs((1+dE)/(1-dE)));
				if (Math.abs(newD) == Infinity || Math.abs(newD)>radiusD) {
					newD = radiusD;
				}
				var newX:Number = newD*Math.cos(Math.atan2(dy1, dx1));
				var newY:Number = newD*Math.sin(Math.atan2(dy1, dx1));
			}
			var obj:Object = {x:newX, y:newY, scale:newD};
			return obj;
		}
	}
}
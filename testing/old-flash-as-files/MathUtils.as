package com
{

	/**
	 * A few math calculations
	 * @author Luke Mrphy
	 *
	 */
	public class MathUtils
	{

	public function MathUtils() {

	}

	public function returnFunction(q:Number):Number {
		var r:Number = Math.sqrt(q);
		return r;
	}

	public static function fibO(n : Number) : Number {
	//1,1,2,3,5,8,13...,
	// Get Fib at position n
		if (n == 1 || n == 2) {
			return 1;
		} else {
			return fibO(n-1)+fibO(n-2);
		}
	}

	public static function Phi():Number {
		return (Math.sqrt(5))/2;
	}


	public static function Random(arg0 : Number, arg1 : Number) : Number {

		var returnNumber : Number = 0;
		if (arg1 == 0) {
			returnNumber = Math.round(Math.random()* arg0);
		} else {
			returnNumber = arg0 + Math.round(Math.random()* (arg1 - arg0));
		}

		return returnNumber;

	}

	public static function perspectiveRatio(z : Number, d : Number) : Number {
		var pr : Number = d/(d+z);
		return pr;
	}
	}
}
package com.younglibin.reverse;

public class ReverseString {

	/**
	 * @author libin
	 * @time 2014-2-17 下午2:36:07
	 * @return void
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		ReverseString rs = new ReverseString();
		String re = rs.reverse("libin");
		System.out.println("re:" + re);
	}

	public String reverse(String str) {
		if (null == str || str.length() == 1) {
			return str;
		}
		return reverse(str.substring(1)) + str.charAt(0);
	}
}

package com.myapache.common;

import org.apache.commons.codec.digest.DigestUtils;


/**
 * MD5 加密 是一个不可逆的过程， 如果要验证， 两个密码是否相等，只能将 两个密码分别计算MD5 比较MD5 是否相等
 * @author libin
 * @time 2014-2-27 上午10:39:33
 */
public class TestMd5 {

	/**
	 * @author libin
	 * @time 2014-2-27 上午10:08:52
	 * @return void
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String md5str = DigestUtils.md5Hex("123456");
		System.out.println("md5str:" + md5str);
	}
}

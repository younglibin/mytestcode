package com.younglibin.study.test2;

public class Bar extends Foo {
	public int a;

	public Bar() {
		a = 8;
	}

	public void addFive() {
		this.a += 5;
	}

	public static void main(String[] args) {
		Foo foo = new Bar();
		System.out.println("1===Value: " + foo.a);
		foo.addFive();
		System.out.println("Value: " + foo.a);
	}

}

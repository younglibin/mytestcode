package com.younglibin.study.extendsTest;

public class Dog extends Animal {
	public void print() {
		System.out.println("super:"
				+ this.getClass().getSuperclass().getName().hashCode());
		super.print();
		// System.out.println("name hashcode:" + name.hashCode());
		age = 20;
		name = "baibei";
		System.out.println("name hashcode:" + name.hashCode());
		super.print();
	}
}

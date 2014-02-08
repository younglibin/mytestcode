package com.younglibin.study.extendsTest;

public class Cat extends Animal {

	public void print() {
		System.out.println("super:"
				+ this.getClass().getSuperclass().getName().hashCode());
		super.print();
		//System.out.println("name hashcode:" + name.hashCode());
		age = 10;
		name = "mimi";
		System.out.println("name hashcode:" + name.hashCode());
		super.print();
	}
}

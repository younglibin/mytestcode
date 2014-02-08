package com.younglibin.study.extendsTest;

public class Cat2 {
	public Animal animal = new Animal();

	public void print() {
		System.out.println("super:"
				+ this.getClass().getSuperclass().getName().hashCode());
		animal.print();
		// System.out.println("name hashcode:" + name.hashCode());
		animal.age = 10;
		animal.name = "mimi";
		System.out.println("name hashcode:" + animal.name.hashCode());
		animal.print();
	}
}

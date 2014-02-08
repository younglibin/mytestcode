package com.younglibin.study.extendsTest;

public class Animal {
	public String name;
	public int age;

	public void print() {
		System.out.println("name:" + name + "\tage:" + age);
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public int getAge() {
		return age;
	}

	public void setAge(int age) {
		this.age = age;
	}
	
	
}

package com.younglibin.study.extendsTest;

public class Client {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Animal cat = new Cat();
		Animal dog = new Dog();
		cat.print();
		System.out.println("==========================");
		dog.print();

		System.out.println("==========================");
		System.out.println("cat --> animal:"
				+ cat.getClass().getSuperclass().hashCode());
		System.out.println("dog --> animal:"
				+ dog.getClass().getSuperclass().hashCode());
		System.out.println("dog.superClass equal cat.supercalss:"
				+ dog.getClass().getSuperclass()
						.equals(cat.getClass().getSuperclass()));

		System.out.println("dog.superClass == cat.supercalss:"
				+ (dog.getClass().getSuperclass() == cat.getClass()
						.getSuperclass()));
	}

}

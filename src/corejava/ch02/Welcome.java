package corejava.ch02;


/**
 * ��һ��corejava��һ������
  * @ClassName: Welcome  
  * @Description: TODO 
  * @author: libin 
  * @date:Oct 23, 2012 1:46:13 PM
 */
public class Welcome {

	/**
	 * ��ڷ���
	  * @Title: main  
	  * @Description: TODO 
	  * @param args 
	  * @return void 
	  * @author: libin  
	  * @date:Oct 23, 2012 1:46:41 PM 
	  * @throws
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String[] strArray = new String[3];
		
		strArray[0]="Welcome to  Core Java";
		strArray[1]="by  libin ";
		strArray[2]="and lb";
		for(String str:strArray){
			System.out.println(str);
		}
	}

}

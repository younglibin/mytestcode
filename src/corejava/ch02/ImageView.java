package corejava.ch02;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;

import javax.swing.ImageIcon;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

/**
 * 	ͼƬ�鿴
  * @ClassName: ImageView  
  * @Description: TODO 
  * @author: libin 
  * @date:Oct 23, 2012 1:34:05 PM
 */
public class ImageView {

	/**
	 * ��ڷ���
	  * @Title: main  
	  * @Description: TODO 
	  * @param args   ����
	  * @return void  ����
	  * @author: libin  
	  * @date:Oct 23, 2012 1:35:44 PM 
	  * @throws
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
			JFrame frame = new ImageViewerFrame();
			frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			frame.setVisible(true);
	}
}
/**
 * �ڲ���
  * @ClassName: ImageViewerFrame  
  * @Description: TODO 
  * @author: libin 
  * @date:Oct 23, 2012 1:34:29 PM
 */
	class ImageViewerFrame extends JFrame{
		private JLabel  lab;
		private JFileChooser chooser;
		private static final int DEFAULT_WIDTH=300;
		private static final int DEFAULT_HEIGHT=400;
		public ImageViewerFrame(){
			this.setTitle("ImageView");
			this.setSize(DEFAULT_WIDTH, DEFAULT_HEIGHT);
			lab = new JLabel();
			this.add(lab);
			
			chooser = new JFileChooser();
			chooser.setCurrentDirectory(new File("."));
			
			JMenuBar mb = new JMenuBar();
			this.setJMenuBar(mb);
			
			JMenu jm = new JMenu("File");
			mb.add(jm);
			
			JMenuItem jmi  = new JMenuItem("Open");
			jm.add(jmi);
			
			jmi.addActionListener(new ActionListener(){
				public void actionPerformed(ActionEvent e) {
					// TODO Auto-generated method stub
					int result = chooser.showOpenDialog(null);
					if(result == JFileChooser.APPROVE_OPTION){
						String name = chooser.getSelectedFile().getPath();
						lab.setIcon(new ImageIcon(name));
					}
				}
				
			});
			
			JMenuItem exit = new JMenuItem("Exit");
			jm.add(exit);
			exit.addActionListener(new ActionListener(){

				public void actionPerformed(ActionEvent e) {
					// TODO Auto-generated method stub
					System.exit(0);
				}
			});
			
		}
	}



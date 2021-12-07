package com.example.LibraryShop;

import java.util.regex.Pattern;
import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;
import org.apache.commons.io.FileUtils;
import java.io.File;

public class TheTests {
  private WebDriver driver;
  private String baseUrl;
  private boolean acceptNextAlert = true;
  private StringBuffer verificationErrors = new StringBuffer();
  JavascriptExecutor js;
  @Before
  public void setUp() throws Exception {
	  System.setProperty("webdriver.chrome.driver", "lib\\win\\chromedriver.exe");
    driver = new ChromeDriver();
    baseUrl = "https://www.google.com/";
    driver.manage().timeouts().implicitlyWait(60, TimeUnit.SECONDS);
    js = (JavascriptExecutor) driver;
  }

  @Test
  public void testAddRemoveChapter() throws Exception {
    driver.get("http://3.135.240.54/");
    driver.findElement(By.linkText("Login")).click();
    driver.findElement(By.name("username")).clear();
    driver.findElement(By.name("username")).sendKeys("admin");
    driver.findElement(By.id("id_password")).clear();
    driver.findElement(By.id("id_password")).sendKeys("admin");
    driver.findElement(By.id("id_submit")).click();
    driver.findElement(By.linkText("Administration page")).click();
    driver.findElement(By.xpath("//div[@id='content-main']/div[2]/table/tbody/tr[2]/td/a")).click();
    driver.findElement(By.id("id_book_id")).click();
    new Select(driver.findElement(By.id("id_book_id"))).selectByVisibleText("Pride and Prejudice by Jane Austen");
    driver.findElement(By.id("id_chapter_title")).click();
    driver.findElement(By.id("id_chapter_title")).clear();
    driver.findElement(By.id("id_chapter_title")).sendKeys("testChapter");
    driver.findElement(By.id("id_chapter_num")).click();
    driver.findElement(By.id("id_chapter_num")).clear();
    driver.findElement(By.id("id_chapter_num")).sendKeys("0");
    driver.findElement(By.id("id_price")).click();
    driver.findElement(By.id("id_price")).clear();
    driver.findElement(By.id("id_price")).sendKeys("2");
    
    Thread.sleep(2500);	

    WebElement upload_file = driver.findElement(By.xpath("//input[@id='id_file']"));
    upload_file.sendKeys("C:\\Users\\yskin\\chapter.txt");
    Thread.sleep(2000);

    driver.findElement(By.name("_save")).click();
    driver.findElement(By.name("_selected_action")).click();
    driver.findElement(By.xpath("//table[@id='result_list']/tbody/tr/th/a")).click();
    driver.findElement(By.linkText("Delete")).click();
    Thread.sleep(2000);
    driver.findElement(By.xpath("//input[@value='Yes, I’m sure']")).click();
    
    Thread.sleep(2500);	
  }

  @Test
  public void testAddRemoveUser() throws Exception {
    driver.get("http://3.135.240.54/");
    driver.findElement(By.linkText("Login")).click();
    driver.findElement(By.name("username")).clear();
    driver.findElement(By.name("username")).sendKeys("admin");
    driver.findElement(By.id("id_password")).clear();
    driver.findElement(By.id("id_password")).sendKeys("admin");
    driver.findElement(By.id("id_submit")).click();
    driver.findElement(By.linkText("Administration page")).click();
    driver.findElement(By.xpath("//div[@id='content-main']/div/table/tbody/tr[2]/td/a")).click();
    driver.findElement(By.id("id_username")).clear();
    driver.findElement(By.id("id_username")).sendKeys("yahya");
    driver.findElement(By.id("id_password1")).clear();
    driver.findElement(By.id("id_password1")).sendKeys("123456Yah");
    driver.findElement(By.id("id_password2")).clear();
    driver.findElement(By.id("id_password2")).sendKeys("123456Yah");
    driver.findElement(By.name("_save")).click();
    driver.findElement(By.xpath("//nav[@id='nav-sidebar']/div/table/tbody/tr[2]/th/a")).click();
    
    Thread.sleep(1500);	
    
    driver.findElement(By.linkText("yahya")).click();
    driver.findElement(By.linkText("Delete")).click();
    driver.findElement(By.xpath("//input[@value='Yes, I’m sure']")).click();
    
    Thread.sleep(1500);	
  }

  @Test
  public void testAdminAddRemoveAuthor() throws Exception {
    driver.get("http://3.135.240.54/");
    
    driver.findElement(By.linkText("Login")).click();
    driver.findElement(By.name("username")).clear();
    driver.findElement(By.name("username")).sendKeys("admin");
    driver.findElement(By.id("id_password")).clear();
    driver.findElement(By.id("id_password")).sendKeys("admin");
    driver.findElement(By.id("id_submit")).click();
    
    Thread.sleep(1500);	
    
    driver.findElement(By.linkText("Administration page")).click();
    driver.findElement(By.xpath("//div[@id='content-main']/div[2]/table/tbody/tr/td/a")).click();
    driver.findElement(By.id("id_firstname")).click();
    driver.findElement(By.id("id_firstname")).clear();
    driver.findElement(By.id("id_firstname")).sendKeys("Charles");
    driver.findElement(By.id("id_lastname")).clear();
    driver.findElement(By.id("id_lastname")).sendKeys("Bukowski");
    driver.findElement(By.name("_save")).click();
    
    Thread.sleep(1500);	

    driver.findElement(By.name("_selected_action")).click();
    new Select(driver.findElement(By.name("action"))).selectByVisibleText("Delete selected authors");
    driver.findElement(By.name("index")).click();
    
    Thread.sleep(1500);	

    driver.findElement(By.xpath("//input[@value='Yes, I’m sure']")).click();
  }

  @Test
  public void testCreateCollectionDup() throws Exception {
    driver.get("http://3.135.240.54/");
    
  //Login first 
    driver.get("http://3.135.240.54/");
    driver.findElement(By.linkText("Login")).click();
    driver.findElement(By.name("username")).click();
    driver.findElement(By.name("username")).clear();
    driver.findElement(By.name("username")).sendKeys("admin");
    driver.findElement(By.id("id_password")).clear();
    driver.findElement(By.id("id_password")).sendKeys("admin");
    driver.findElement(By.id("id_submit")).click();
    
    driver.findElement(By.linkText("Create Collections")).click();
    driver.findElement(By.id("id_name")).click();
    driver.findElement(By.id("id_name")).clear();
    driver.findElement(By.id("id_name")).sendKeys("My Books");
    driver.findElement(By.xpath("//*/text()[normalize-space(.)='']/parent::*")).click();
    new Select(driver.findElement(By.id("id_book_choices"))).selectByVisibleText("Book with Three Chapters by Exam Ple");
    driver.findElement(By.xpath("//option[@value='3']")).click();
    driver.findElement(By.xpath("//option[@value='1']")).click();
    driver.findElement(By.xpath("//option[@value='2']")).click();
    driver.findElement(By.xpath("//input[@value='Create Collection']")).click();
  }

  @Test
  public void testDownloadBook() throws Exception {
	  
	  driver.manage().window().maximize();
	  
	  //Login first 
	    driver.get("http://3.135.240.54/");
	    driver.findElement(By.linkText("Login")).click();
	    driver.findElement(By.name("username")).click();
	    driver.findElement(By.name("username")).clear();
	    driver.findElement(By.name("username")).sendKeys("admin");
	    driver.findElement(By.id("id_password")).clear();
	    driver.findElement(By.id("id_password")).sendKeys("admin");
	    driver.findElement(By.id("id_submit")).click();
	    
	    
    driver.findElement(By.linkText("My Books")).click();
    driver.findElement(By.linkText("Think Python")).click();
    //driver.findElement(By.cssSelector("a[href='/book/3']")).click();

    driver.findElement(By.linkText("[[DOWNLOAD]]")).click();
  }

  @Test
  public void testLogInLogOut() throws Exception {
    driver.get("http://3.135.240.54/");
    driver.findElement(By.linkText("Login")).click();
    driver.findElement(By.name("username")).clear();
    driver.findElement(By.name("username")).sendKeys("admin");
    driver.findElement(By.id("id_password")).clear();
    driver.findElement(By.id("id_password")).sendKeys("admin");
    driver.findElement(By.id("id_submit")).click();
    
    Thread.sleep(2500);	
    
    driver.findElement(By.id("logo_title")).click();
    driver.findElement(By.linkText("Logout [admin]")).click();
  }

  @Test
  public void testSearchAuthorNameAusten() throws Exception {
    driver.get("http://3.135.240.54/");
    driver.findElement(By.linkText("Search Books")).click();
    driver.findElement(By.id("id_title")).click();
    driver.findElement(By.id("id_title")).clear();
    driver.findElement(By.id("id_title")).sendKeys("Pride");
    driver.findElement(By.xpath("//form[@id='search_form']/p[2]")).click();
    driver.findElement(By.id("footer")).click();
    driver.findElement(By.xpath("//input[@value='Search']")).click();
  }
  
  @Test
  public void testSearchGenreRomance() throws Exception {
    driver.get("http://3.135.240.54/");
    driver.findElement(By.linkText("Search Books")).click();
    new Select(driver.findElement(By.id("id_genre"))).selectByVisibleText("Romance");
    driver.findElement(By.xpath("//input[@value='Search']")).click();
  }
  
  @Test
  public void testSearchJaneAusten() throws Exception {
    driver.get("http://3.135.240.54/search");
    driver.findElement(By.linkText("Search Books")).click();
    new Select(driver.findElement(By.id("id_author"))).selectByVisibleText("Jane Austen");
    driver.findElement(By.xpath("//option[@value='1']")).click();
    driver.findElement(By.xpath("//input[@value='Search']")).click();
  }
	
  @Test
  public void testSearchByDate() throws Exception {
    driver.get("http://3.135.240.54/");
	//driver.manage().window().maximize();

    driver.findElement(By.linkText("Search Books")).click();

    driver.findElement(By.id("id_search_date_before")).sendKeys("12062021");
    driver.findElement(By.xpath("//input[@value='Search']")).click();
  }

  
  @After
  public void tearDown() throws Exception {
    driver.quit();
    String verificationErrorString = verificationErrors.toString();
    if (!"".equals(verificationErrorString)) {
      fail(verificationErrorString);
    }
  }

  private boolean isElementPresent(By by) {
    try {
      driver.findElement(by);
      return true;
    } catch (NoSuchElementException e) {
      return false;
    }
  }

  private boolean isAlertPresent() {
    try {
      driver.switchTo().alert();
      return true;
    } catch (NoAlertPresentException e) {
      return false;
    }
  }

  private String closeAlertAndGetItsText() {
    try {
      Alert alert = driver.switchTo().alert();
      String alertText = alert.getText();
      if (acceptNextAlert) {
        alert.accept();
      } else {
        alert.dismiss();
      }
      return alertText;
    } finally {
      acceptNextAlert = true;
    }
  }
}



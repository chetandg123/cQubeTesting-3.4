import time
import unittest
from selenium.webdriver.support.select import Select
from Locators.parameters import Data


from cQube_Dashboard.Attendance.student_attendance.student_attendance_report import student_attendance_report
from reuse_func import GetData


class cQube_Student_Attendance_regression(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.data = GetData()

        self.driver = self.data.get_driver()
        self.data.open_cqube_appln(self.driver)
        self.data.login_cqube(self.driver)
        self.data.navigate_to_student_report()
        year = Select(self.driver.find_element_by_id(Data.sar_year))
        month = Select(self.driver.find_element_by_id(Data.sar_month))
        self.year = year.first_selected_option.text
        self.month = month.first_selected_option.text
        self.driver.implicitly_wait(100)

    def test_click_on_student_attendence_report(self):
        sar = student_attendance_report(self.driver,self.year,self.month)
        result = sar.click_on_sar()
        if "Student Attendance Infra_Table_Report" in self.driver.page_source:
            print("Navigating to Student Attendance Infra_Table_Report is working")
        else:
            print("Student_Attendance page does not exist!...")

    def test_click_on_blocks(self):
        block = student_attendance_report(self.driver,self.year,self.month)
        result = block.check_markers_on_block_map()
        self.assertNotEqual(0, len(result) - 1, msg="Dots are not present on map")
        print("Blocks button is working")
        print("Markers are present on the map")

        cluster = student_attendance_report(self.driver,self.year,self.month)
        result = cluster.check_markers_on_clusters_map()
        self.assertNotEqual(0, len(result) - 1, msg="Dots are not present on map")
        print("Clusters button is working")
        print("Markers are present on the map")

        school = student_attendance_report(self.driver,self.year,self.month)
        result = school.check_markers_on_schools_map()
        self.assertNotEqual(0, int(len(result) - 1), msg="Dots are not present on map")
        print("Schools button is working")
        print("Markers are present on the map")

    def test_districtwise_csv_download(self):
        csv = student_attendance_report(self.driver, self.year, self.month)
        result = csv.click_download_icon_of_district()
        self.assertEqual(0,result,msg='Mis match found at footer information')
        print('Districtwise csv file is downloaded')
        self.data.page_loading(self.driver)

    def test_blockwise_csv_download(self):
        csv = student_attendance_report(self.driver, self.year, self.month)
        result = csv.click_download_icon_of_blocks()
        if result==0:
            print("Block wise csv report download is working")
        else:
            raise self.failureException("Block wise csv report download is not working")
        time.sleep(2)

    def test_clusterwise_csv_download(self):
        csv = student_attendance_report(self.driver, self.year, self.month)
        result = csv.click_download_icon_of_clusters()
        if result:
            print("Cluster wise csv report download is working")
            csv.remove_csv()
        else:
            raise self.failureException("Cluster wise csv report download is not working")

    def test_schoolwise_csv_download(self):
        csv = student_attendance_report(self.driver, self.year, self.month)
        result = csv.click_download_icon_of_schools()
        if result:
            print("School wise csv report download is working")
            csv.remove_csv()
        else:
            raise self.failureException("School wise csv report download is not working")

    def test_choose_district_block_cluster(self):
        time.sleep(3)
        dist = student_attendance_report(self.driver, self.year, self.month)
        result = dist.check_districts_csv_download()
        if result == 0:
            print("Block per district csv report download is working")
            print("on selection of each district")
            print("The footer value of no of schools and no of students are")
            print("equals to downloaded file")
        else:
            raise self.failureException("Block per district csv report download is working")

        block = student_attendance_report(self.driver, self.year, self.month)
        result = block.check_csv_download()
        if result == 0:
            print("Cluster per block csv report download is working")
            print("on selection of each district and block")
            print("The footer value of no of schools and no of students are")
            print("equals to downloaded file")
        else:
            raise self.failureException("Cluster per block csv report download is working")
        schools = student_attendance_report(self.driver, self.year, self.month)
        result = schools.check_district_block_cluster()
        if result == 0:
            print("Schools per cluster csv download report is working")
            print("on selection of each district,block and cluster")
            print("The footer value of no of schools and no of students are")
            print("equals to downloaded file")
        else:
            raise self.failureException("Schools per cluster csv report download is working")

    def test_check_hyperlinks(self):
        hyperlinks = student_attendance_report(self.driver,self.year,self.month)
        result1,result2,choose_dist= hyperlinks.click_on_hyperlinks()
        # if res0ult1 == False and result2 == False and choose_dist == "Choose a District " :
        #     pri0nt("hyperlinks are working")
        # else :00
        #     raise self.failureException("hyperlinks are not working")

    def test_home_icon(self):
        home = student_attendance_report(self.driver,self.year,self.month)
        home.click_on_blocks_click_on_home_icon()
        result = home.click_HomeButton()
        if "student-attendance" in result:
            print("Home Icon is working")
        else:
            raise self.failureException('Home Icon is not working')
        self.data.page_loading(self.driver)

    def test_total_no_of_students_and_total_no_of_schools_is_equals_at_blocks_clusters_schools(self):
        tc = student_attendance_report(self.driver,self.year,self.month)
        student_count, Bstudents,school_count,Bschools = tc.check_blocklevel_total_no_of_students()
        self.assertEqual(int(student_count), int(Bstudents), msg="Block level no of students are not equal")
        self.assertEqual(int(school_count), int(Bschools), msg="Block level no of schools are not equal to no of schools ")

        student_count, Cstudents,school_count,Cschool = tc.check_clusterlevel_total_no_of_students()
        self.assertEqual(int(student_count), int(Cstudents), msg="Cluster level no of students are not equal")
        self.assertEqual(int(school_count), int(Cschool), msg="Cluster level no of schools are not equal to no of schools ")

        student_count, Sstudents,school_count,Sschool = tc.check_schoollevel_total_no_of_students()
        self.assertEqual(int(student_count), int(Sstudents), msg="Cluster level no of students are not equal")
        self.assertEqual(int(school_count), int(Sschool), msg="Cluster level no of schools are not equal to no of schools ")
        print("Total number of students and school equals on clicking of blocks,clusters,schools")


    def test_logout(self):
        logout = student_attendance_report(self.driver,self.year,self.month)
        result = logout.click_on_logout()
        self.assertEqual("Log in to cQube", result, msg="login page is not exist!..")
        print("Logout Functionality is working")
        self.data.login_cqube(self.driver)
        time.sleep(1)
        self.data.navigate_to_student_report()
        self.data.page_loading(self.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

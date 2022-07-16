/* 
 *  test.c - vi du ve linux kernel module
 */

#include <linux/module.h> /* thu vien nay dinh nghia cac macro nhu module_init va module_exit */

#define DRIVER_AUTHOR "Nguyen Anh Duy <anhduy20072000@gmail.com>"
#define DRIVER_DESC   "A sample loadable kernel module"


static int __init init_start(void)
{
    printk("Start Embedded\n");
    return 0;
}

static void __exit exit_finish(void)
{
    printk("Finish Embedded\n");
}

module_init(init_start);
module_exit(exit_finish);

MODULE_LICENSE("GPL"); /* giay phep su dung cua module */
MODULE_AUTHOR(DRIVER_AUTHOR); /* tac gia cua module */
MODULE_DESCRIPTION(DRIVER_DESC); /* mo ta chuc nang cua module */
MODULE_SUPPORTED_DEVICE("testdevice"); /* kieu device ma module ho tro */

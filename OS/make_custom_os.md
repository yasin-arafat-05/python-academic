
একটি নিজস্ব কাস্টম ওএস তৈরি করতে হলে প্রধানত ৩টি জিনিস লাগে:
 1. Kernel (kernel): ওএসের মূল চালিকাশক্তি বা মস্তিষ্ক।
 2. Root Filesystem (rootfs): ওএসের ফাইল এবং প্রোগ্রামগুলো যেখানে থাকে।
 3. Bootloader (যেমন GRUB, QEMU বা syslinux): কম্পিউটার চালু হওয়ার পর ওএস-কে মেমোরিতে লোড করার জন্য।
নিচে আপনার অনুরোধ অনুযায়ী সম্পূর্ণ ফাইল স্ট্রাকচার এবং স্ক্রিনশটের সব কমান্ডের বিস্তারিত ব্যাখ্যা দেওয়া হলো।


<br>
<br>

# `1. Kernel Configuration:`

<br>
<br>

## ১. কাস্টম ওএস-এর ফাইল স্ট্রাকচার (File Structure)
আপনার কাস্টম ডিস্ট্রোর কাজের সুবিধার জন্য নিচের মতো একটি পরিষ্কার ডিরেক্টরি স্ট্রাকচার তৈরি করে নেওয়া ভালো:

```txt
my_custom_distro/
├── build/                 # কার্নেল এবং রুট ফাইলসিস্টেম বিল্ড করার মূল ডিরেক্টরি
│   ├── linux-6.12.58/    # এক্সট্রাক্ট করা লিনাক্স কার্নেলের সোর্স কোড
│   └── rootfs/            # আপনার ওএসের মূল ফাইল স্ট্রাকচার (নিচে বিস্তারিত)
│       ├── bin/           # প্রয়োজনীয় কমান্ড (যেমন: sh, ls, cd)
│       ├── sbin/          # সিস্টেম কমান্ড (যেমন: init)
│       ├── dev/           # ডিভাইস ফাইলস (যেমন: console, null)
│       ├── etc/           # কনফিগারেশন ফাইলস
│       ├── proc/          # কার্নেল প্রসেস ইনফরমেশন ডিরেক্টরি
│       ├── sys/           # সিস্টেম ইনফরমেশন ডিরেক্টরি
│       └── usr/           # অন্যান্য ইউজার প্রোগ্রাম
└── output/                # ফাইনাল বুটেবল ওএস ইমেজ যেখানে জমা হবে
    └── bzImage            # কম্পাইল করা ফাইনাল কার্নেল ফাইল (এটাই আপনার ওএস রান করবে)
```
> বাস্তব উদাহরণ: একটি নতুন ফ্ল্যাট বা বাড়িতে জিনিসপত্র রাখার জন্য রান্নাঘর, শোবার ঘর, আর ড্রয়িংরুম আলাদা করে সাজানো।
> 
লিনাক্স এলোমেলো কোনো ফাইল পছন্দ করে না। এর একটি নির্দিষ্ট ডিরেক্টরি স্ট্রাকচার বা ঘর আছে, যাকে FHS (Filesystem Hierarchy Standard) বলে। 

| ফোল্ডারের নাম | কাজ কী? (সহজ ভাষায়) |
| :--- | :--- |
| /bin (Binaries) | এখানে কম্পিউটারের মূল কমান্ড বা চালিকা ফাইলগুলো থাকে (যেমন Toybox-এর ফাইলটি এখানে থাকবে)। |
| /lib (Libraries) | বিভিন্ন প্রোগ্রাম চলার জন্য যে শেয়ার্ড কোড বা লাইব্রেরির প্রয়োজন হয়, সেগুলো এখানে থাকে (Windows-এর .dll ফাইলের মতো)। |
| /dev (Devices) | লিনাক্সে সবকিছুই একটি ফাইল। তোমার মাউস, কিবোর্ড, পেনড্রাইভ, এমনকি হার্ডডিস্ককেও লিনাক্স এই ফোল্ডারের ভেতরে একেকটি ভার্চুয়াল ফাইল হিসেবে দেখায়। |
| /proc (Process) | এটি কোনো আসল হার্ডডিস্কের জায়গা নেয় না। কার্নেল বর্তমানে কী কাজ করছে, র‍্যাম কতটা খালি আছে, প্রসেসরের তাপমাত্রা কত—এইসব লাইভ তথ্য এই ফোল্ডারের ফাইলগুলোতে জমা থাকে। |
| /etc (Editable Text Configuration) | তোমার সিস্টেমের সব সেটিংস বা কনফিগারেশন ফাইল এই ফোল্ডারে থাকে। যেমন- কোন ইউজার লগইন করতে পারবে, তার পাসওয়ার্ড কী ইত্যাদি। |


## ২. লিনাক্স কার্নেল (Kernel) কেন দরকার?
খুব সহজ ভাষায়, কার্নেল হলো একটি ওএসের মূল মস্তিষ্ক বা হার্ট।
আপনি যখন কিবোর্ডে কোনো কি (Key) চাপেন, কিংবা মনিটরে কিছু দেখতে চান—তখন আপনার ওএসের সফটওয়্যার সরাসরি কম্পিউটারের হার্ডওয়্যারের (CPU, RAM, GPU) সাথে কথা বলতে পারে না। মাঝখানে একজন দোভাষী বা ম্যানেজারের প্রয়োজন হয়। লিনাক্স কার্নেল ঠিক এই কাজটিই করে। এটি আপনার কাস্টম ওএসের সফটওয়্যার এবং কম্পিউটারের হার্ডওয়্যারের মধ্যে সেতু বন্ধন তৈরি করে। কার্নেল ছাড়া কোনো অপারেটিং সিস্টেমই বুট বা চালু হতে পারবে না।

## ৩. সবগুলো কমান্ড এবং বিস্তারিত ব্যাখ্যা
আপনার স্ক্রিনশটগুলোতে যে ধাপগুলো দেখানো হয়েছে, তার প্রতিটি কমান্ডের কারণ নিচে ব্যাখ্যা করা হলো:
### ধাপ ১: সোর্স কোড ডাউনলোড ও এক্সট্রাক্ট:
 * cd my_custom_distro/build 
   * কেন: আপনার ওএসের সোর্স কোডগুলো গোছানো রাখার জন্য build নামের ফোল্ডারে প্রবেশ করা হয়েছে।""
 * Search in google "linx kenel archives" link: https://www.kernel.org/ 
 * copy the link of LTS Version -> Long Term Suport that is stable.
 * wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.18.35.tar.xz
   * কেন: লিনাক্সের অফিশিয়াল ওয়েবসাইট থেকে একদম খাঁটি লিনাক্স কার্নেলের সোর্স কোড (ভার্সন 6.12.58) ডাউনলোড করার কমান্ড। এটি একটি কমপ্রেসড (.tar.xz) ফাইল হিসেবে ডাউনলোড হয়।
 * tar xf linux-6.12.58.tar.xz
   * কেন: ডাউনলোড করা কমপ্রেসড ফাইলটি আনজিপ বা এক্সট্রাক্ট করার জন্য। এর ফলে মূল সোর্স কোডের ফোল্ডারটি বের হয়ে আসে। Xf menas এক্সট্রাক্ট file. 
 * rm *.tar.xz
   * কেন: এক্সট্রাক্ট করার পর মূল জিপ ফাইলটির আর প্রয়োজন নেই, তাই মেমোরি খালি করার জন্য ওটা ডিলিট করা হয়েছে।
* cd linux-6.12.58.tar.xz
  * For the kernel configuration step.(step-2)


### ধাপ ২: কার্নেল কনফিগারেশন
 * make defconfig
   * কেন: লিনাক্স কার্নেলে হাজার হাজার ফিচার থাকে। আপনার কম্পিউটারের আর্কিটেকচার (যেমন: x86_64 বা ৬৪-বিট) অনুযায়ী একটি def->Default (ডিফল্ট) কনফিগারেশন তৈরি করার জন্য এই কমান্ডটি দেওয়া হয়। এটি একটি .config ফাইল তৈরি করে।
 * make menuconfig
   * কেন: এটি স্ক্রিনে একটি নীল রঙের গ্রাফিক্যাল মেনু (Ncurses UI) ওপেন করে । এর মাধ্যমে আপনি আপনার কাস্টম ওএসে কোন কোন ফিচার বা ড্রাইভার রাখবেন আর কোনটা বাদ দেবেন তা ম্যানুয়ালি ঠিক করতে পারবেন। (যেমন স্ক্রিনশটে গ্রাফিক্স বুট লোগো বা ভার্চুয়াল GPU ড্রাইভার অন/অফ করা হচ্ছে)।
   * If the version is changed the the option is also change. So after doing make menuconfig press / (Slash) and we can search.  Let's search for "DRM_FBDEV_EMULATION" press ENTER.
   * (Enable legacy fbdev support...) সিলেক্ট করলাম, সেটার আসল কাজ হলো: লিনাক্স কার্নেল যখন বুট হবে, তখন সে যেন স্ক্রিনে লেখা বা গ্রাফিক্স দেখানোর জন্য একটি পুরনো কিন্তু খুবই স্টেবল স্ট্যান্ডার্ড (যাকে fbdev বা Framebuffer Device বলে) ব্যবহার করতে পারে।
   কেন এটা দরকার? আমাদের বানানো লিনাক্স ডিস্ট্রিবিউশনটি একদম ছোট ও সিম্পল। এতে বড় কোনো গ্রাফিক্স ড্রাইভার (যেমন এনভিডিয়া বা ফুল ইনটেল ড্রাইভার) নেই। এই অপশনটি অন থাকলে কার্নেল একদম বেসিক মোডে হলেও স্ক্রিনে ডিসপ্লে আউটপুট দিতে পারবে।
   *(graphics support) -> (bootuplogo) (this will see the linux logo while booting)
   * now exit and save the configuration


    
### ধাপ ৩: কম্পাইল এবং রান করা
* make -j8
   * কেন: এটিই আসল জাদুকরী কমান্ড! এটি সোর্স কোডগুলোকে প্রসেস করে বাইনারি বা ওএস ফাইলে রূপান্তর (Compile) করা শুরু করে। এখানে -j8 মানে হলো কম্পাইল করার সময় আপনার প্রসেসরের ৮টি কোর (Core) বা থ্রেড একসাথে ব্যবহার করা হবে, যাতে বিল্ড প্রসেস দ্রুত শেষ হয়।
   * If we get error then. like '127' then use "sudo pacman -S bc". Something to compile linux kernel we don't have all the utilites in our computer. So error may occur. I face ERROR-127.
 * qemu-system-x86_64 -kernel arch/x86/boot/bzImage
   * কেন: কার্নেল সফলভাবে কম্পাইল হওয়ার পর arch/x86/boot/bzImage নামের একটি ফাইল তৈরি হয়। এটিই হলো আপনার ওএসের মূল ফুসফুস। এই কমান্ডটি দিয়ে QEMU Emulator (একটি ভার্চুয়াল মেশিন)-এর মাধ্যমে  আপনার তৈরি করা নতুন ওএস-টিকে টেস্ট বা রান করা হচ্ছে।
  পরবর্তী ধাপে আপনার এই কার্নেলের সাথে যুক্ত করার জন্য একটি Root Filesystem (যেমন: BusyBox ব্যবহার করে) তৈরি করতে হবে। আপনি কি এখন সেই রুট ফাইলসিস্টেম তৈরির কমান্ড এবং প্রক্রিয়াগুলো জানতে চান?
  ```bash
    Kernel: arch/x86/boot/bzImage is ready  (#1)
  ```
  ```bash
    sudo pacman -S qemu-full
  ```
  Test our kernel with qemu-full 
  ```bash
    qemu-system-x86_64 -kernel arch/x86/boot/bzImage
  ```
<br>
<br>

# `2. File System Configuration:`

<br>
<br>

### ধাপ ৪: Toybox ডাউনলোড (Clone) করা:
এবার আমরা আপনার হোম ডিরেক্টরিতে একটা ফোল্ডার বানিয়ে Toybox-এর সোর্স কোড ডাউনলোড করব।
১. টার্মিনালে এই কমান্ডগুলো দিন:
```bash
mkdir -p ~/cloned
cd ~/cloned
git clone --depth 1 https://github.com/landley/toybox.git
cd toybox
```

### ধাপ ৫: Toybox কনফিগার ও কম্পাইল করা
এখানে আমরা Toybox-কে বলব তার ভেতরে থাকা সব কমান্ড যেন সে আমাদের জন্য তৈরি করে।
* ১. ডিফল্ট কনফিগারেশন তৈরি করতে রান করুন:
  * make defconfig
* ২. select all the command list that we want 
  * make menuconfig 
     * from pending (unfinished) commands select the commands. 
* ৩. এবার পুরো কোডটা বিল্ড বা কম্পাইল করার জন্য কমান্ড দিন (এটি ১-২ মিনিট সময় নিতে পারে):
  * make -j$(nproc)
  * *(এখানে -j$(nproc) দেওয়ার মানে হলো আপনার প্রসেসরের সব কয়টি কোর ব্যবহার করে দ্রুত বিল্ড হবে, ঠিক যেমন টিউটোরিয়ালে make -j8 দেওয়া হয়েছিল)*।

### ধাপ ৬: ফাইলসিস্টেম ডিরেক্টরি তৈরি করা (Installation)
* ১. এবার Toybox-এর তৈরি করা কমান্ডগুলো এই নতুন ফোল্ডারে ইনস্টল করুন:
    * PREFIX=~/my_custom_distro/build/rootfs make install
* এখন যদি আপনি ls ~/rootfs কমান্ড দেন, তবে দেখতে পাবেন আপনার তৈরি করা মিনিমাম ডিস্ট্রিবিউশনের জন্য bin, sbin, এবং usr ফোল্ডারগুলো তৈরি হয়ে গেছে!

**Explanation:**
++++++++++++++++

* How user intract with OS
```bash
    User
    ↓
    Shell (sh)
    ↓
    System Calls
    ↓
    Kernel
    ↓
    Hardware
```

* How Boot worked? When we turn on the computer?
```bash
    BIOS/UEFI
    ↓
    Bootloader
    ↓
    Kernel
    ↓
    Init
    ↓
    Shell
```
Kernel boot হওয়ার পরে init চালায়। তারপর init shell (sh) চালায়। Kernel boot হওয়ার পরে init-কে চালায়, আর init user-এর সাথে interaction করার জন্য shell শুরু করে। Shell এবং user programs kernel-এর system call ব্যবহার করে hardware ও system resources access করে । তাহলে আমাদের init টা থাকে sbin এর মধ্যে । তো এখন সেইটা আমাদের trigger করা লাগবে তাই না । 

* এখন, kernel expect করে init আমাদের rootfs এ থাকবে ভাই আমরা একটা symbolic link বানাবো, enter rootfs folder then,
   * ln -s sbin/init init (-s symbolic).
   * ln -s lib lib64 (same)


<br>
<br>

# `3. Shell Configuration:`

<br>
<br>

**কার্নেল একা কিছুই করতে পারে না, তার ইউজার ইন্টারফেস (যেমন শেল) এবং ফাইলসিস্টেম দরকার হয়। আমরা এখানে:**
* **১. শেলের জন্য bash কপি করে অনবো আমার OS থেকে ।**
* **২. শেলের বেঁচে থাকার(dependency) জন্য তার প্রয়োজনীয় লাইব্রেরি বা হাত-পা (.so ফাইলস) সাথে দিলাম।**
* **৩. পুরো জিনিসটাকে একটা পুটলি বা প্যাকেজ (init.cpio) বানালাম।**
* **৪. কার্নেলকে বললাম—"এই নাও তোমার ফাইলসিস্টেম, এবার বুট হয়ে এর ভেতরের init আর sh (শেল) চালু করো।"**

<br>

## ১. ফাইলসিস্টেম সাজানো এবং ডিপেন্ডেন্সি (Libraries) কপি করা
 * **শেল কপি করা:** cp /bin/bash bin/bash এর মাধ্যমে আপনার ল্যাপটপের নিজস্ব bash শেলটিকে কাস্টম ডিরেক্টরির bin/ এর ভেতর কপি করা হলো। (পরের স্ক্রিনশটে এটিকে mv bin/bash bin/sh করে নাম বদলে sh রাখা হয়েছে, কারণ অনেক স্ট্যান্ডার্ড স্ক্রিপ্ট ডিফল্টভাবে /bin/sh খোঁজে)।
 * **ডিপেন্ডেন্সি বা লাইব্রেরি ফিক্স করা:** কোনো বাইনারি ফাইল (যেমন bash বা init) একা চলতে পারে না। তাদের কিছু সহযোগী ফাইল বা শেয়ার্ড লাইব্রেরি (.so ফাইল) লাগে। ldd init এবং ldd bin/bash কমান্ড দিয়ে দেখা হয়েছে এই প্রোগ্রামগুলো চলার জন্য কোন কোন লাইব্রেরি ফাইলের উপর নির্ভরশীল।
 ```bash
    # copy all this into lib folder. 
    ldd init
            linux-vdso.so.1 (0x00007f64d29ac000)
            libcrypt.so.2 => /usr/lib/libcrypt.so.2 (0x00007f64d28d0000)
            libm.so.6 => /usr/lib/libm.so.6 (0x00007f64d279d000)
            libc.so.6 => /usr/lib/libc.so.6 (0x00007f64d2400000)
            /lib64/ld-linux-x86-64.so.2 => /usr/lib64/ld-linux-x86-64.so.2 (0x00007f64d29ae000)

                                                                                                                                                                        
    ~/my_custom_distro/build/rootfs   
    ❯ pwd                                                                        
    /home/yasin/my_custom_distro/build/rootfs
                                                                                                                                                                        
    ~/my_custom_distro/build/rootfs   
    ❯ ls
    bin  init  lib  sbin  usr
                                                                                                    
                                                
    ~/my_custom_distro/build/rootfs   
    ❯ cp /usr/lib64/ld-linux-x86-64.so.2 lib              
                                                                                                                                                                        
    ~/my_custom_distro/build/rootfs   
    ❯ cp /usr/lib/libc.so.6 lib                               
                                                                                                                                                                        
    ~/my_custom_distro/build/rootfs   
    ❯ cp /usr/lib/libm.so.6 lib                  
                                                                                                                                                                        
    ~/my_custom_distro/build/rootfs   
    ❯ cp /usr/lib/libcrypt.so.2 lib                  
                                                                                                                                                                        
    ~/my_custom_distro/build/rootfs   
    ❯ 

    # Do simillary for bin/bash folder 
    but  copy this into usr/bin folder 
    ~/my_custom_distro/build/rootfs   
    ❯ ldd /bin/bash
            linux-vdso.so.1 (0x00007f0bb2743000)
            libreadline.so.8 => /usr/lib/libreadline.so.8 (0x00007f0bb2583000)
            libc.so.6 => /usr/lib/libc.so.6 (0x00007f0bb2200000)
            libncursesw.so.6 => /usr/lib/libncursesw.so.6 (0x00007f0bb2512000)
            /lib64/ld-linux-x86-64.so.2 => /usr/lib64/ld-linux-x86-64.so.2 (0x00007f0bb2745000)

    ❯ mkdir usr/lib

                                                                                                                                                                        
    ~/my_custom_distro/build/rootfs   
    ❯ ldd /bin/bash
            linux-vdso.so.1 (0x00007f0974d51000)
            libreadline.so.8 => /usr/lib/libreadline.so.8 (0x00007f0974b91000)
            libc.so.6 => /usr/lib/libc.so.6 (0x00007f0974800000)
            libncursesw.so.6 => /usr/lib/libncursesw.so.6 (0x00007f0974b20000)
            /lib64/ld-linux-x86-64.so.2 => /usr/lib64/ld-linux-x86-64.so.2 (0x00007f0974d53000)
                                                                                                      # Copy in both lib and user lib folder                                                                    
    ~/my_custom_distro/build/rootfs 
    ❯ cp /usr/lib64/ld-linux-x86-64.so.2 usr/lib                  
                                                                                                                                                                        
    ~/my_custom_distro/build/rootfs   
    ❯ cp /usr/lib/libncursesw.so.6 usr/lib                               
                                                                                                                                                                        
    ~/my_custom_distro/build/rootfs   
    ❯ cp /usr/lib/libc.so.6 usr/lib                         
                                                                                                                                                                        
    ~/my_custom_distro/build/rootfs   
    ❯ cp /usr/lib/libc.so.6 usr/lib                  
                                                                                                                                                                        
    ~/my_custom_distro/build/rootfs   
    ❯ 

```
 * এরপর mkdir lib, mkdir usr/lib তৈরি করে ld-musl-x86_64.so.1, libreadline.so.8, এবং libncursesw.so.6 এর মতো প্রয়োজনীয় লাইব্রেরি ফাইলগুলো বাইরে থেকে কপি করে এই কাস্টম ফাইলসিস্টেমের ভেতর নিয়ে আসা হয়েছে। এগুলো না আনলে বুট করার সময় "File not found" বা ক্র্যাশ মার্ক করত।


## ২. এসেনশিয়াল ডিরেক্টরি ও বুট স্ক্রিপ্ট তৈরি
 * **প্রয়োজনীয় ডিরেক্টরি:** mkdir dev sys etc proc usr/share কমান্ড দিয়ে লিনাক্সের চিরচেনা কিছু ভার্চুয়াল ডিরেক্টরি তৈরি করা হয়েছে। কার্নেল যখন বুট হবে, তখন সে এই ডিরেক্টরিগুলোর ওপর বিভিন্ন ডিভাইস এবং প্রসেস ইনফরমেশন মাউন্ট করবে (যেমনটা  sysfs, proc মাউন্ট করা etc.)।
 * **স্টার্টআপ স্ক্রিপ্ট:** vim etc/init.d/rcS ফাইলটি তৈরি করা হচ্ছে। Linux কোনো ফাইল চালানোর সময় .sh, .exe, .txt দেখে না। বরং দেখে: i) ফাইলটি executable কি না (chmod +x) ii) ফাইলের শুরুতে shebang আছে কি না যেমনঃ #!/bin/sh এই গুলো । লিনাক্স বুট হওয়ার পর শুরুর দিকের স্ক্রিপ্ট বা কনফিগারেশন রান করানোর জন্য এই ফাইলটি ব্যবহৃত হয়।
 * **What I have in the rcS file:** Some mount using the command we can see my current rsC files mount: 
 ```bash
   mount | more 
 ```
 But in the below table all the 

| Filesystem   | Mount Command                     | কাজ কী?                                                                                      | উদাহরণ                                         |
| ------------ | --------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| **proc**     | `mount -t proc proc /proc`        | Kernel এবং running process-এর তথ্য দেখায়। এটি একটি virtual filesystem, ডিস্কে থাকে না।       | `cat /proc/cpuinfo`, `cat /proc/meminfo`, `ps` |
| **sysfs**    | `mount -t sysfs sysfs /sys`       | Kernel, device এবং driver সম্পর্কিত তথ্য প্রদান করে। Hardware management-এর জন্য ব্যবহৃত হয়। | `ls /sys/class`, `ls /sys/block`               |
| **devtmpfs** | `mount -t devtmpfs devtmpfs /dev` | Device file তৈরি করে দেয়, যাতে kernel ও user-space device access করতে পারে।                  | `/dev/null`, `/dev/tty`, `/dev/sda`            |
| **tmpfs**    | `mount -t tmpfs tmpfs /tmp`       | RAM-এ temporary file সংরক্ষণ করে। Reboot করলে সব data মুছে যায়।                              | `/tmp/test.txt`, temporary cache files         |

### সহজ ভাষায়

| Directory | যদি Mount না করো তাহলে কী সমস্যা হবে?                                                                                |
| --------- | -------------------------------------------------------------------------------------------------------------------- |
| **/proc** | `ps`, `top`, `free`, `cat /proc/*` কাজ করবে না।                                                                      |
| **/sys**  | Hardware ও driver information পাওয়া যাবে না।                                                                         |
| **/dev**  | Terminal (`/dev/tty`), disk (`/dev/sda`), null device (`/dev/null`) ইত্যাদি পাওয়া যাবে না; shell-ও সমস্যা করতে পারে। |
| **/tmp**  | অনেক program temporary file তৈরি করতে পারবে না।                                                                      |
For a custom distro-র জন্য সবচেয়ে গুরুত্বপূর্ণ হলো:
```sh
# mount -t (type) proc  /proc (final folder)
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev
```
এগুলো প্রায় সব Linux system-এ boot-এর সময় mount করা হয়। `tmpfs` optional, কিন্তু রাখা ভালো।
finally make the file executable:
```bash
 chmod +x init
 chmod +x etc/init.d/rcS
```
**This folder will be automatically run by init.**


## ৩. ফাইলসিস্টেমকে প্যাকেজ করা (Archive) এবং QEMU-তে রান করা
শেষের স্ক্রিনশটগুলোতে পুরো ফাইলসিস্টেমটাকে কার্নেলের পড়ার উপযোগী করে প্যাকিং করা হচ্ছে এবং তা টেস্ট করা হচ্ছে:
 * CPIO আর্কাইভ তৈরি: cpio হচ্ছে একটি আর্কাইভ টুল (যেমনটা tar বা zip হয়)। rootfs যেতে find command দিলে যেসব file পাবো সবগুলোকে আমাকে package হিসেবে convert করতে হবে । "rootfs" থেকে commadn টা দিতে হবে ।  এর জন্য নিচের command টা ব্যবহার করবো ভাই । find | cpio -o -H newc > ../init.cpio কমান্ডের মাধ্যমে এতক্ষণ ধরে তৈরি করা সমস্ত ডিরেক্টরি, লাইব্রেরি, init, এবং শেলকে একসঙ্গে প্যাক করে init.cpio নামের একটি ফাইলে রূপান্তর করা হলো। লিনাক্স কার্নেল বুট হওয়ার সময় এই ফরম্যাটের ফাইল সরাসরি মেমরিতে লোড করতে পারে, যাকে initramfs বলা হয়।

 * কার্নেল ও ফাইলসিস্টেম বুট করা: সবশেষে qemu-system-x86_64 কমান্ড দিয়ে একটি ভার্চুয়াল মেশিনে লিনাক্স কার্নেল (bzImage) এবং আমাদের বানানো ফাইলসিস্টেম (init.cpio) একসাথে বুট করা হচ্ছে। command টা আগের মতো করো kernel folder এ গিয়ে দিতে হবে ভাই । 


**Must be we get error please solve this via: Go to the rootfs folder then**
```bash
❯ sudo chroot . /sbin/init                                
```


### সংক্ষেপে কেন এগুলো দরকার ছিল?
কার্নেল একা কিছুই করতে পারে না, তার ইউজার ইন্টারফেস (যেমন শেল) এবং ফাইলসিস্টেম দরকার হয়। আমরা এখানে:
১. শেলের জন্য bash কপি করে আনলাম।
২. শেলের বেঁচে থাকার জন্য তার প্রয়োজনীয় লাইব্রেরি বা হাত-পা (.so ফাইলস) সাথে দিলাম।
৩. পুরো জিনিসটাকে একটা পুটলি বা প্যাকেজ (init.cpio) বানালাম।
৪. কার্নেলকে বললাম—"এই নাও তোমার ফাইলসিস্টেম, এবার বুট হয়ে এর ভেতরের init আর sh (শেল) চালু করো।"




<br>
<br>

# `3. Display Server and Protocol and Desktop Environment:`

<br>
<br>



## ১. Wayland কী এবং এটা কেন দরকার? (Why Wayland?)
সহজ কথায়, Wayland হলো একটি মডার্ন ডিসপ্লে সার্ভার প্রোটোকল। এটি আপনার লিনাক্স সিস্টেমের ভেতরের ব্যাকএন্ডে কাজ করে। এর একমাত্র কাজ হলো: আপনার মাউস-কিবোর্ডের ইনপুট নেওয়া, সেটা অ্যাপকে পাঠানো এবং অ্যাপের গ্রাফিক্স বা উইন্ডোটাকে স্ক্রিনে নিখুঁতভাবে ফুটিয়ে তোলা।
### কেন আগের সিস্টেম (X11) বাদ দিয়ে Wayland ব্যবহার করা হচ্ছে?
লিনাক্সে প্রায় ৩০-৪০ বছর ধরে X11 (X Org) নামের একটা পুরোনো ডিসপ্লে সার্ভার ব্যবহার করা হতো। কিন্তু আধুনিক কম্পিউটারের জন্য X11-এ কিছু বড় সমস্যা ছিল, যা সমাধান করতেই Wayland এসেছে

## ২. Wayland বনাম Desktop Environment (DE): পার্থক্য কী?
অনেকে মনে করেন Wayland বুঝি নিজেই একটা ডেস্কটপ বা উইন্ডো ম্যানেজার। আসলে তা নয়। এদের সম্পর্কটা বুঝতে এই তুলনাটি দেখুন:
> বাস্তব উদাহরণ: একটা গাড়ির কথা চিন্তা করুন।
>  * Wayland হলো গাড়ির ইঞ্জিন ও চ্যাসিস (Engine & Chassis): যা ভেতরের মূল মেকানিজম বা শক্তি সরবরাহ করে, কিন্তু আপনি সরাসরি এটাতে বসেন না বা দেখেন না।
>  * Desktop Environment হলো গাড়ির বডি, ড্যাশবোর্ড, সিট এবং এসি (Interior & Body): যা আপনি চোখে দেখেন, টাচ করেন এবং ব্যবহার করেন।
> 
নিচে এদের মূল পার্থক্যগুলোর একটি ছক দেওয়া হলো:

| বৈশিষ্ট্য | Wayland (ডিসপ্লে সার্ভার/প্রোটোকল) | Desktop Environment (DE) |
| :--- | :--- | :--- |
| মূল ভূমিকা | এটি পর্দার আড়ালে (Backend) গ্রাফিক্সের পাইপলাইন এবং সিকিউরিটি হ্যান্ডেল করে। | এটি আপনার সামনে (Frontend) সম্পূর্ণ গ্রাফিক্যাল ইউজার ইন্টারফেস তৈরি করে। |
| আপনি যা দেখেন | এর নিজস্ব কোনো দৃশ্যমান রূপ বা বাটন নেই। এটি জাস্ট একটা মেকানিজম। | আপনি বুট করার পর যা দেখেন—টাস্কবার, অ্যাপ্লিকেশন মেনু, সেটিংস অ্যাপ, ওয়ালপেপার, ফাইল ম্যানেজার ইত্যাদি। |
| উপাদানসমূহ | এটি মূলত একটি ডিসপ্লে প্রোটোকল এবং কম্পোজিটর (যেমন আপনার স্ক্রিনশটের wlroots বা tinywl)। | এটি অনেকগুলো অ্যাপের কালেকশন (যেমন: GNOME, KDE Plasma, XFCE)। |
| উদাহরণ | Wayland, X11। | GNOME, KDE Plasma, Cinnamon, XFCE। |

### এরা একসাথে কীভাবে কাজ করে?
আপনি যখন আপনার পছন্দের কোনো ডেস্কটপ এনভায়রনমেন্ট (যেমন KDE Plasma বা GNOME) ব্যবহার করেন, তখন সেই ডিস্ট্রোর ভেতরে গ্রাফিক্স দেখানোর ইঞ্জিন হিসেবে ব্যাকগ্রাউন্ডে Wayland কাজ করে।
আপনি যেহেতু কাস্টম লিনাক্স বানাচ্ছেন, আপনি সরাসরি কোনো ভারী Desktop Environment (যেমন KDE/GNOME) ইন্সটল না করে, একদম রূঢ় বা মিনিমাল লেভেলে একটা Wayland কম্পোজিটর (tinywl বা Sway) দিয়ে আপনার নিজস্ব কাস্টম ইন্টারফেস বা DE দাঁড় করাচ্ছেন।



## লিনাক্স গ্রাফিক্স ও বিল্ড সিস্টেমের মূল উপাদানসমূহ

| নাম (Component) | এটি আসলে কী? (What it is) | বাস্তব উদাহরণ (Real-world Example) | এটি না থাকলে কী হতো? (What if it's missing?) |
| :--- | :--- | :--- | :--- |
| Daemon (ড্যামন) | লিনাক্সের ব্যাকগ্রাউন্ডে বা পর্দার আড়ালে চলতে থাকা স্বয়ংক্রিয় প্রোগ্রাম বা সার্ভিস। এর কোনো ভিজ্যুয়াল উইন্ডো থাকে না। | একটি রেস্টুরেন্টের পেছনের বাবুর্চি, যাকে আপনি সরাসরি দেখেন না কিন্তু সে অনবরত খাবার তৈরি করে যাচ্ছে। (যেমন: seatd, bluetoothd)। | ব্যাকগ্রাউন্ডের স্বয়ংক্রিয় কাজগুলো (যেমন পেনড্রাইভ ঢোকালে ডিটেক্ট করা, ব্লুটুথ কানেক্ট করা) প্রতিবার আপনাকে ম্যানুয়ালি কমান্ড লিখে করতে হতো। |
| Display Protocol (ডিসপ্লে প্রোটোকল) | স্ক্রিনে গ্রাফিক্স দেখানোর জন্য একটি নিয়ম বা যোগাযোগের ভাষা। অ্যাপগুলো ডিসপ্লে সার্ভারের সাথে কীভাবে কথা বলবে, তা এটি ঠিক করে। | যেমন Wayland বা পুরোনো X11। এটি অনেকটা ট্রাফিক নিয়মের মতো, যা গাড়িগুলোকে (অ্যাপগুলোকে) কীভাবে চলতে হবে তা বলে দেয়। | অ্যাপগুলো ডিসপ্লে সার্ভারকে বোঝাতে পারতো না যে তারা স্ক্রিনের ঠিক কোন জায়গায়, কতটুকু সাইজের উইন্ডো দেখাতে চায়। |
| Display Server / Compositor (ডিসপ্লে সার্ভার) | লিনাক্সে এই দুটি মূলত একই কাজ করে (বিশেষ করে Wayland-এ)। এটি স্ক্রিনের পিক্সেল ম্যানেজ করে, সব অ্যাপের উইন্ডোকে একসাথে সাজিয়ে স্ক্রিনে ফুটিয়ে তোলে। | একটি আর্ট গ্যালারির কিউরেটর, যে ঠিক করে কোন ছবিটা (উইন্ডো) দেয়ালে কোথায় ঝুলবে এবং একটার ওপর আরেকটা কীভাবে থাকবে। | আপনি স্ক্রিনে কোনো গ্রাফিক্যাল উইন্ডো, মাউস কার্সার বা ওয়ালপেপার দেখতে পারতেন না। শুধু কালো স্ক্রিনে সাদা টেক্সট (TTY CLI) থাকত। |
| wlroots | Wayland ডিসপ্লে সার্ভার বা কম্পোজিটর সহজে বানানোর জন্য একটি তৈরি করা কোডের লাইব্রেরি বা টুলকিট। | একটি রেডিমেড বাড়ি বানানোর কিট। যেখানে দেয়াল, পিলার রেডি থাকে; আপনি শুধু নিজের মতো ডিজাইন করে রঙ করেন। | প্রতিবার নতুন উইন্ডো ম্যানেজার (যেমন Sway, Hyprland) বানানোর জন্য ডেভেলপারদের গ্রাফিক্সের হাজার হাজার লাইনের জটিল কোড একদম শূন্য থেকে নতুন করে লিখতে হতো। |
| tinywl | wlroots লাইব্রেরি ব্যবহার করে বানানো পৃথিবীর সবচেয়ে ছোট ও মিনিমাল একটা এক্সাম্পল Wayland উইন্ডো ম্যানেজার। | একটি খেলনা গাড়ি বা ডেমো প্রোটোটাইপ, যা দিয়ে শুধু টেস্ট করা যায় যে ইঞ্জিনটা ঠিকঠাক কাজ করছে কিনা। | আপনার কাস্টম লিনাক্সে গ্রাফিক্স ঠিকঠাক কাজ করছে কিনা তা পরীক্ষা করার জন্য আপনাকে সরাসরি জটিল এবং বড় কোনো উইন্ডো ম্যানেজার (যেমন Sway) সেটআপ করতে হতো। |
| Seat (সীট) | একটি কম্পিউটারে গ্রাফিক্স, মাউস, কিবোর্ড এবং অডিওর সমন্বয়ে তৈরি হওয়া একটি কমপ্লিট ইউজার সেশন বা কাজের জায়গা। | একটি কম্পিউটারের সাথে যুক্ত এক সেট মনিটর, কিবোর্ড আর মাউস। একই পিসিতে একাধিক সেট থাকলে সেগুলোকে Seat0, Seat1 বলা হয়। | লিনাক্স সিকিউরলি ট্র্যাক করতে পারতো না যে কোন মাউস বা কিবোর্ডটি এই মুহূর্তে গ্রাফিক্যাল স্ক্রিনকে কন্ট্রোল করছে। |
| Meson & Ninja | সোর্স কোডকে সফটওয়্যারে রূপান্তর (Compile) করার আধুনিক ও সুপার-ফাস্ট বিল্ড সিস্টেম টুলস। | Meson হলো ব্লুপ্রিন্ট বা প্ল্যানার (যে নকশা করে কী কী লাগবে), আর Ninja হলো দ্রুত কাজ করা রাজমিস্ত্রি (যে বিল্ড বা কম্পাইল করে)। | আপনাকে হাজার হাজার C ফাইলের জন্য ম্যানুয়ালি জটিল gcc কমান্ড লিখে ঘণ্টার পর ঘণ্টা বসে কোড কম্পাইল করতে হতো। |

### এদের মধ্যকার সম্পর্কটা একটু সহজে বুঝুন:
ধরুন, আপনি আপনার কাস্টম লিনাক্সে একটি ব্রাউজার ওপেন করলেন। পুরো প্রসেসটা যেভাবে কাজ করে:
১. ব্রাউজারটি Wayland (Display Protocol) এর ভাষায় ডিসপ্লে সার্ভারের সাথে যোগাযোগ করে।
২. ব্যাকগ্রাউন্ডে থাকা seatd (Daemon) আপনার মাউস ও কিবোর্ডের ইনপুটকে Seat এর মাধ্যমে পারমিশন দেয়।
৩. tinywl (Compositor), যা কিনা wlroots দিয়ে তৈরি, সেটি ব্রাউজারের উইন্ডোটিকে স্ক্রিনের সঠিক জায়গায় সুন্দরভাবে সাজিয়ে (Composite করে) আপনাকে দেখায়।

# Wayland configratin command:

## ১. Wayland ব্যাকএন্ড (wlroots) সোর্স কোড ডাউনলোড ও কম্পাইল করা
একটি মিনিমাল গ্রাফিক্যাল উইন্ডো ম্যানেজার চালানোর জন্য আমাদের একটি ডিসপ্লে সার্ভার লাগবে। এখানে wlroots ব্যবহার করা হয়েছে, যা এই গ্রাফিক্সের মূল ভিত্তি হিসেবে কাজ করে। https://gitlab.freedesktop.org/wlroots/wlroots. see the letest version from this.

In my arch i don't have wlroots. So, 1st install on my machine.
```bash
sudo pacman -S wlroots0.20
```
Then find the same version from the above link: 
```bash
    cd ~/releases/build/
    wget https://gitlab.freedesktop.org/wlroots/wlroots/-/archive/0.20.0/wlroots-0.20.0.tar.gz
```

 * কেন দরকার: wlroots এর সোর্স কোডটি ইন্টারনেট থেকে ডাউনলোড করার জন্য wget ব্যবহার করা হয়েছে।
 * কাজের ধরন: wlroots-0.18.2.tar.gz নামের একটি কম্প্রেসড ফাইল ডাউনলোড হয়।
```bash
    tar -xf wlroots-0.20.0.tar.gz
    rm *.tar.gz
    mv wlroots-0.20.0 wlroots
    cd wlroots/
```
 * কেন দরকার: ডাউনলোড করা ফাইলটি জিপ করা থাকে, সেটাকে আনজিপ বা এক্সট্র্যাক্ট করে ফোল্ডার গোছানোর জন্য।
 * কাজের ধরন: tar xf দিয়ে ফাইলটি এক্সট্র্যাক্ট করা হয়েছে, rm দিয়ে জিপ ফাইলটি মুছে ফেলা হয়েছে, এবং সহজে কাজ করার জন্য ফোল্ডারের নাম পরিবর্তন করে শুধু wlroots রাখা হয়েছে।

## ২. Meson ও Ninja দিয়ে সোর্স কোড বিল্ড/কম্পাইল করা
*see the README.md file where we have the latest command if anything changes. And make sure meson and ninja is present on your computer.*
সোর্স কোড তো নামানো হলো, কিন্তু কম্পিউটার সরাসরি C বা C++ সোর্স কোড বোঝে না। একে বাইনারি বা এক্সিকিউটেবল ফাইলে রূপান্তর (Compile) করতে হবে। এর জন্য meson (বিল্ড কনফিগারেশন টুল) এবং ninja (কম্পাইলার রানার) ব্যবহার করা হয়েছে। 
meson setup build

 * কেন দরকার: এটি আপনার সিস্টেমে wlroots কম্পাইল করার জন্য প্রয়োজনীয় সব ডিপেন্ডেন্সি (যেমন: লাইব্রেরি, হেডার ফাইল) আছে কিনা তা পরীক্ষা করে এবং একটি build ডিরেক্টরি তৈরি করে।
ninja -C build/

 * কেন দরকার: এটি আসল কম্পাইলেশনের কাজ শুরু করে। C কোডগুলোকে প্রসেস করে বাইনারি ফাইল এবং এক্সিকিউটেবল রেডি করে।
 * কাজের ধরন: -C build/ মানে হচ্ছে ninja-কে বলা হচ্ছে build ফোল্ডারের ভেতরে ঢুকে কাজ করতে।

## ৩. তৈরি হওয়া গ্রাফিক্যাল এক্সিকিউটেবলগুলো আপনার কাস্টম ডিস্ট্রোতে কপি করা
কম্পাইল শেষ হওয়ার পর build ফোল্ডারে কিছু রেডিমেড এক্সাম্পল বা মিনিমাল কম্পোজিটর তৈরি হয় (যেমন simple এবং tinywl)। এগুলোকে আপনার কাস্টম লিনাক্সের ফাইল সিস্টেমে (rootfs/bin/) নিতে হবে।

```bash
    cd my_custom_distro/build/wlroots/build
    cp tinywl/tinywl  ~/my_custom_distro/build/rootfs/bin
    cp examples/simple  ~/my_custom_distro/build/rootfs/bin
```
 * কেন দরকার: আপনার তৈরি করা কাস্টম লিনাক্স যখন বুট হবে, তখন যেন সে এই গ্রাফিক্যাল প্রোগ্রামগুলো খুঁজে পায় এবং চালাতে পারে।
 * কাজের ধরন: cp (copy) কমান্ড দিয়ে ফাইল দুটিকে আপনার কাস্টম ডিস্ট্রোর মূল বাইনারি ফোল্ডারে পাঠানো হয়েছে। tinywl হলো একটি অতি ক্ষুদ্র উইন্ডো ম্যানেজার, যা দিয়ে আপনি স্ক্রিনে উইন্ডো ওপেন করতে পারবেন।

## ৪. শেয়ার্ড লাইব্রেরি (Shared Libraries / .so files) ম্যানেজমেন্ট
গ্রাফিক্যাল প্রোগ্রামগুলো (যেমন tinywl) একা একা চলতে পারে না। এদের চলার জন্য লিনাক্স সিস্টেমের অনেকগুলো শেয়ার্ড লাইব্রেরি বা .so (Shared Object) ফাইলের প্রয়োজন হয় (যেমন গ্রাফিক্স ড্রাইভার, মেমোরি ম্যানেজমেন্ট ইত্যাদি)। After going rootfs give the comand 
ldd bin/tinywl | vim - (use ia)

## 5. udevd and seatd configuration:

I am using arch so from the packman cache we can directly fetch the necessary files. 
| সার্ভিস (Service) | সংজ্ঞা (Definition) | প্রধান কাজ (Main Task) | কেন দরকার (Why Needed) |
| --- | --- | --- | --- |
| **udevd** | এটি লিনাক্সের একটি ব্যাকগ্রাউন্ড ডেমন (Device Manager Daemon), যা সিস্টেমে কোনো নতুন হার্ডওয়্যার যুক্ত বা বিচ্ছিন্ন হলে তা স্বয়ংক্রিয়ভাবে সনাক্ত করে। | `/dev/` ডিরেক্টরির অধীনে হার্ডওয়্যারগুলোর জন্য সঠিক ডিভাইস নোড (যেমন: মাউস, কিবোর্ড, গ্রাফিক্স কার্ডের ফাইল) তৈরি করে। | এটি ছাড়া কার্নেল মাউস, কিবোর্ড বা ডিসপ্লে পোর্টকে ফাইল হিসেবে চিনতে পারে না; ফলে গ্রাফিক্যাল সার্ভার কোনো ইনপুট ডিভাইস খুঁজে পায় না। |
| **seatd** | এটি একটি মিনিমাল সিট ম্যানেজমেন্ট ডেমন (Seat Management Daemon), যা মাল্টিমিডিয়া এবং গ্রাফিক্স ডিভাইসের পারমিশন ও এক্সেস কন্ট্রোল নিরাপদে হ্যান্ডেল করে। | রুট প্রিভিলেজ (Root privilege) ছাড়া সাধারণ ইউজার বা `tinywl`-কে গ্রাফিক্স কার্ড এবং ইনপুট ডিভাইস সরাসরি ব্যবহারের নিরাপদ অনুমতি (Permission) দেয়। | এটি ছাড়া Wayland কম্পোজিটর (যেমন `tinywl`) ভিডিও কার্ড এবং মাউস-কিবোর্ড সরাসরি এক্সেস করার অনুমতি পায় না, যার ফলে গ্রাফিক্স মোড অন হতে পারে না। |

```bash
sudo tar -I zstd -xf /var/cache/pacman/pkg/seatd-*.pkg.tar.zst --strip-components=0
# check that seatd copy or not:
ls -l usr/bin/seatd
ls -l usr/lib/libseat.so*

# now install udev from arch linux:
~/my_custom_distro/build/rootfs   
❯ cp -a /usr/lib/systemd/systemd-udevd sbin/udevd
                                                             
~/my_custom_distro/build/rootfs   
❯ cp -a /usr/bin/udevadm bin/
                                                           
~/my_custom_distro/build/rootfs   
❯ cp -a /usr/lib/udev etc/
    
~/my_custom_distro/build/rootfs   
❯ 

```
Now in the init Script file:
```bash
# udev configuration:
/sbin/udevd --daemon
/bin/udevadm trigger --action=add
/bin/udevadm settle --timeout=5
```
<br>

Also crate a folder named run, this folder will be tepporary brohter:
```bash
mount -t tmpfs tmpfs /run -o mode=0755,nosuid,nodev
```

<br>

Create root user:
```bash
# here 0 means: root user
❯ echo "root:x:0:0:root:/root:/bin/sh" >> etc/passwd

<br>

```
## 6. Now, configure mouse keyboard etc in RAM Memory:

**give the command from rootfs folder**

| ফাইলের নাম / ডিরেক্টরি | লিনাক্স ওএসে এর আসল পরিচয় (Identity) | কেন এটি ছাড়া ওএসে গ্রাফিক্স চলবে না? (The Core Reason) |
| --- | --- | --- |
| **`mkdir -p run/user/0`** 0 means root users.| এটি র‍্যামের (RAM) ওপর তৈরি হওয়া একটি অত্যন্ত সুরক্ষিত এবং অস্থায়ী ফোল্ডার। | ডিসপ্লে সার্ভার (`tinywl`) এবং গ্রাফিক্যাল অ্যাপগুলোর (যেমন: টার্মিনাল, ব্রাউজার) মধ্যে যোগাযোগের জন্য একটি **"চিঠির বাক্স"** বা **সকেট ফাইল** তৈরি করতে হয়। এই বিশেষ ফাইলটি রাখার জন্য এই ডিরেক্টরি বাধ্যতামূলক। |
| **`export XDG_RUNTIME_DIR`** | এটি একটি এনভায়রনমেন্ট ভেরিয়েবল (Environment Variable) বা ওএসের নির্দেশিকা। | এটি দিয়ে ওএস এবং সব অ্যাপকে আগে থেকে জানিয়ে দেওয়া হয় যে, *"ভাই, গ্রাফিক্সের যোগাযোগের চিঠির বাক্সটা কিন্তু ওই `/run/user/0` ফোল্ডারে রাখা আছে।"* এটি না জানালে অ্যাপগুলো ডিসপ্লে সার্ভারকে খুঁজেই পাবে না। |
| **`/usr/share/X11/xkb`** | এটি হলো কিবোর্ডের বাটন বা লেআউটের একটি **ভাষার অভিধান (Dictionary)**। | কিবোর্ডের হার্ডওয়্যার চাপলে ওএস শুধু কাঁচা কোড পায় (যেমন: `30` বা `28`)। কিন্তু এই `30` মানে যে **'A'** আর `28` মানে যে **'Enter'**—তা অনুবাদ করার জন্য এই ফোল্ডারটি দরকার। এটি না থাকলে গ্রাফিক্স অন হলেও কিবোর্ড পুরো অচল হয়ে থাকবে। |

---

### 🧱 পুরো গ্রাফিক্স সিস্টেমের কাজের চেইন (Summary)

আপনার ওএসে গ্রাফিক্স পুরোপুরি সচল হতে এই ৪টি জিনিস ব্যাকগ্রাউন্ডে ক্রমান্বয়ে কাজ করে:

1. **`udevd`** $\rightarrow$ মাউস, কিবোর্ড ও গ্রাফিক্স কার্ডের হার্ডওয়্যার তারগুলো খুঁজে বের করে ওএসে যুক্ত করে।
2. **`seatd`** $\rightarrow$ রুট ছাড়া সাধারণ ইউজার বা ডিসপ্লে সার্ভারকে ওই হার্ডওয়্যারগুলো সরাসরি ব্যবহার করার পারমিশন দেয়।
3. **`XDG_RUNTIME_DIR`** $\rightarrow$ ডিসপ্লে সার্ভার ও অ্যাপসের যোগাযোগের জন্য 'চিঠির বাক্স' বা সকেট তৈরির জায়গা দেয়।
4. **`X11/xkb`** $\rightarrow$ কিবোর্ডের বাটনের ভাষা অনুবাদ করে ওএস-কে টাইপ করতে সাহায্য করে।
এই ৪টা জিনিসের যেকোনো একটা মিস হলেই কিন্তু আপনার ওএসের গ্রাফিক্যাল স্ক্রিন আর অন হবে না ভাই!

--- 


```bash                                                                  
~/my_custom_distro/build/rootfs   
❯ mkdir -p run/user/0
                                                                                                                                                                       
~/my_custom_distro/build/rootfs   
❯ echo 'export XDG_RUNTIME_DIR=/run/user/0' >> root/.bashrc
zsh: no such file or directory: root/.bashrc
                                                                                                                                                                       
~/my_custom_distro/build/rootfs   
❯ echo 'export XDG_RUNTIME_DIR=/run/user/0' > root/.bashrc
zsh: no such file or directory: root/.bashrc
                                                                                                                                                                       
~/my_custom_distro/build/rootfs   
❯ mkdir -p root      
                                                                                                                                                                       
~/my_custom_distro/build/rootfs   
❯ echo 'export XDG_RUNTIME_DIR=/run/user/0' > root/.bashrc


# this is for globally profile:
echo 'export XDG_RUNTIME_DIR=/run/user/0' >> etc/profile
                                                                                                                                                                      
~/my_custom_distro/build/rootfs   
❯ mkdir -p usr/share/
                                                                                                                                                     
~/my_custom_distro/build/rootfs   
❯ sudo cp -r /usr/share/X11/ usr/share/                                                        
```

### crate a video group and change the init-script file:
```bash
echo "video:x:985:" >> etc/group

# change the rcS script like this: 
# udev configuration:
export LD_LIBRARY_PATH=/usr/lib:/usr/lib/systemd

/sbin/udevd --daemon
/bin/udevadm trigger --action=add
/bin/udevadm settle --timeout=5

# seatd daemon স্টার্ট করুন (udev এর পরে):
echo "[+] Starting seatd daemon..."
seatd -g video -u root &
sleep 1
```

### See this:(if you face problem. ) If there is no griphcs then our wayland will not work brohter.

```bash
~/my_custom_distro/build/linux-6.18.35   
❯ ls -la | grep config
-rw-r--r--   1 yasin yasin       59 Jun  9 16:28 .cocciconfig
-rw-r--r--   1 yasin yasin   147042 Jun 19 11:28 .config
-rw-r--r--   1 yasin yasin   146277 Jun 19 11:07 .config.old
-rw-r--r--   1 yasin yasin      575 Jun  9 16:28 .editorconfig
-rw-r--r--   1 yasin yasin      582 Jun  9 16:28 Kconfig
                                                                                                                                                                       
~/my_custom_distro/build/linux-6.18.35   
❯ grep -i "CONFIG_DRM" .config
CONFIG_DRM=y
# CONFIG_DRM_DEBUG_MM is not set
CONFIG_DRM_MIPI_DSI=y
CONFIG_DRM_KMS_HELPER=y
# CONFIG_DRM_PANIC is not set
CONFIG_DRM_CLIENT=y
CONFIG_DRM_CLIENT_LIB=y
CONFIG_DRM_CLIENT_SELECTION=y
CONFIG_DRM_CLIENT_SETUP=y
CONFIG_DRM_FBDEV_EMULATION=y
CONFIG_DRM_FBDEV_OVERALLOC=100
# CONFIG_DRM_CLIENT_LOG is not set
CONFIG_DRM_CLIENT_DEFAULT_FBDEV=y
CONFIG_DRM_CLIENT_DEFAULT="fbdev"
# CONFIG_DRM_LOAD_EDID_FIRMWARE is not set
CONFIG_DRM_DISPLAY_HELPER=y
# CONFIG_DRM_DISPLAY_DP_AUX_CEC is not set
# CONFIG_DRM_DISPLAY_DP_AUX_CHARDEV is not set
CONFIG_DRM_DISPLAY_DP_HELPER=y
CONFIG_DRM_DISPLAY_DSC_HELPER=y
CONFIG_DRM_DISPLAY_HDCP_HELPER=y
CONFIG_DRM_DISPLAY_HDMI_HELPER=y
CONFIG_DRM_TTM=y
CONFIG_DRM_BUDDY=y
CONFIG_DRM_GEM_SHMEM_HELPER=y
# CONFIG_DRM_EFIDRM is not set
# CONFIG_DRM_SIMPLEDRM is not set
# CONFIG_DRM_VESADRM is not set
# CONFIG_DRM_RADEON is not set
# CONFIG_DRM_AMDGPU is not set
# CONFIG_DRM_NOUVEAU is not set
CONFIG_DRM_I915=y
CONFIG_DRM_I915_FORCE_PROBE=""
CONFIG_DRM_I915_CAPTURE_ERROR=y
CONFIG_DRM_I915_COMPRESS_ERROR=y
CONFIG_DRM_I915_USERPTR=y
CONFIG_DRM_I915_REQUEST_TIMEOUT=20000
CONFIG_DRM_I915_FENCE_TIMEOUT=10000
CONFIG_DRM_I915_USERFAULT_AUTOSUSPEND=250
CONFIG_DRM_I915_HEARTBEAT_INTERVAL=2500
CONFIG_DRM_I915_PREEMPT_TIMEOUT=640
CONFIG_DRM_I915_PREEMPT_TIMEOUT_COMPUTE=7500
CONFIG_DRM_I915_MAX_REQUEST_BUSYWAIT=8000
CONFIG_DRM_I915_STOP_TIMEOUT=100
CONFIG_DRM_I915_TIMESLICE_DURATION=1
# CONFIG_DRM_XE is not set
# CONFIG_DRM_VGEM is not set
# CONFIG_DRM_VKMS is not set
# CONFIG_DRM_VMWGFX is not set
# CONFIG_DRM_GMA500 is not set
# CONFIG_DRM_UDL is not set
# CONFIG_DRM_AST is not set
# CONFIG_DRM_MGAG200 is not set
# CONFIG_DRM_QXL is not set
CONFIG_DRM_VIRTIO_GPU=y
CONFIG_DRM_VIRTIO_GPU_KMS=y
CONFIG_DRM_PANEL=y
# CONFIG_DRM_PANEL_RASPBERRYPI_TOUCHSCREEN is not set
CONFIG_DRM_BRIDGE=y
CONFIG_DRM_PANEL_BRIDGE=y
# CONFIG_DRM_I2C_NXP_TDA998X is not set
# CONFIG_DRM_ANALOGIX_ANX78XX is not set
# CONFIG_DRM_ETNAVIV is not set
# CONFIG_DRM_HISI_HIBMC is not set
# CONFIG_DRM_APPLETBDRM is not set
# CONFIG_DRM_BOCHS is not set
# CONFIG_DRM_CIRRUS_QEMU is not set
# CONFIG_DRM_GM12U320 is not set
# CONFIG_DRM_VBOXVIDEO is not set
# CONFIG_DRM_GUD is not set
# CONFIG_DRM_ST7571_I2C is not set
# CONFIG_DRM_SSD130X is not set
CONFIG_DRM_PANEL_ORIENTATION_QUIRKS=y
# CONFIG_DRM_ACCEL is not set
                                                                                                                                                                       
~/my_custom_distro/build/linux-6.18.35   
❯ 
```


````bash
sudo pacman -S mgba-sdl
cp /usr/bin/mgba ~/my_custom_distro/build/rootfs/usr/bin/
chmod +x ~/my_custom_distro/build/rootfs/usr/bin/mgba

# copy all the dependency:
sudo cp -v /usr/lib/libmgba.so* \
/usr/lib/libSDL2-2.0.so* \
/usr/lib/libedit.so* \
/usr/lib/libGL.so* \
/usr/lib/libGLX.so* \
/usr/lib/libpng16.so* \
/usr/lib/libzip.so* \
/usr/lib/libsqlite3.so* \
/usr/lib/libelf.so* \
/usr/lib/liblua*.so* \
/usr/lib/libavcodec.so* \
/usr/lib/libavformat.so* \
/usr/lib/libavutil.so* \
/usr/lib/libswscale.so* \
/usr/lib/libswresample.so* \
~/my_custom_distro/build/rootfs/lib/

# downlaod the game 
# https://frzit.itch.io/google-dino-advance
curl -L -o ~/my_custom_distro/build/rootfs/root/game.gba https://github.com/frzit/google-dino-advance/raw/main/build/google-dino-advance.gba

```





<div id="faq_1"  class="ui black segment">
    <div class="header"><h4>1. WeJudge（以下简称OJ）运行在什么平台下？支持哪些语言？</h4></div>
    <div class="content">
        目前为止，WeJudge运行在Linux平台下，支持C、C++两种语言，编译器环境分别为GNU GCC和GNU G++。<br><br>
        <strong>评测机设置的编译参数为：</strong><br><br>
        C语言：<span class="text-danger">gcc -ansi -fno-asm -Wall -std=c99 -lm</span><br>
        C++语言：<span class="text-danger">g++  -ansi -fno-asm -Wall -lm --static</span><br>
        Java：<span class="text-danger">javac -encoding utf-8 (Version:1.8)</span><br><br>
        特别提醒：Java语言请将公共类的名称定义为Main，并且需要编写入口函数main()，否则无法评测。
    </div>
</div>
<div id="faq_2" class="ui black segment">
    <div class="header"><h4>2. 我提交了程序，OJ回复的那些评判结果是什么意思？</h4></div>
    <div class="content">
        下面是常见的OJ评判结果以及它们表示的意思：<br><br>
        <div class="ui relaxed divided list">
            <div class="item">
               <h4>Q. 队列中(Queuing)</h4>
               <p>提交太多了，OJ无法在第一时间给所有提交以评判结果，后面提交的程序将暂时处于排队状态等待OJ的评判。<br>不过这个过程一般不会很长。如果这个状态长时间没有改变，请及时与管理员、老师联系。</p>
            </div>
            <div class="item">
               <h4>R. 运行中(Running)</h4>
               <p>您的程序正在OJ上运行。如果这个状态长时间没有改变，请及时与管理员、老师联系。</p>
            </div>
            <div class="item">
               <h4>1. 评测通过(Accepted)</h4>
               <p>恭喜你，你的代码运行测试数据后反馈的结果与题目预设的参考结果完全吻合。</p>
            </div>
            <div class="item">
               <h4>2. 格式错误(Presentation Error)</h4>
               <p>表示评测机发现您的答案在格式上有问题。<br>
                虽然您的程序貌似输出了正确的结果，但是这个结果的格式有点问题，并不能和参考结果完全吻合。<br>
                请检查程序的输出是否多了或者少了空格（'&nbsp;'）、制表符（'\t'）或者换行符（'\n'）。</p>
            </div>
            <div class="item">
               <h4>3. 超过时间限制(Time Limit Exceeded)</h4>
               <p>表示您的程序运行的时间已经超出了这个题目的时间限制。<br>
                请检查您的程序代码。有可能是因为循环没有及时终止，或者算法不是最优的，时间复杂度高等。</p>
            </div>
            <div class="item">
               <h4>4. 超过内存限制(Memory Limit Exceeded)</h4>
               <p>表示您的程序运行的内存已经超出了这个题目的内存限制。<br>
                请检查您的程序代码。是不是数组开大了？递归函数深度太高？</p>
            </div>
            <div class="item">
               <h4>5. 答案错误(Wrong Answer)</h4>
               <p>表示评测机发现你的答案与参考数据不匹配。<br>
                请检查您的程序代码。是算法写错了？没看清楚题目？还是因为数据精确度不够导致误差？<br>
                请记住，判题机会逐个字检查您程序的输出答案，哪怕错了一个字符，都会认为答案是错误的。</p>
            </div>
            <div class="item">
               <h4>6. 运行时错误(Runtime Error)</h4>
               <p>表示您的程序在运行期间执行了非法的操作。<br>
                请检查您的程序代码。数组越界、无限制递归、除数为0、非法内存操作、浮点数超限、栈溢出等问题都将引发运行时错误</p>
            </div>
            <div class="item">
               <h4>7. 输出内容超限(Output Limit Exceeded)</h4>
               <p>表示您的程序输出内容太多，超过了这个题目的输出限制。<br>
                请检查您的程序代码。通常，如果程序输出的内容超过题目参考答案内容的2倍大小，则引发此错误。</p>
            </div>
            <div class="item">
               <h4>8. 编译错误(Compilation Error)</h4>
               <p>表示您的程序语法有问题，编译器无法编译。<br>
                请检查您的程序代码。你可以在评测机报告中查看编译器反馈的错误信息。</p>
            </div>
            <div class="item">
               <h4 class="list-group-item-heading">9. 系统错误(System Error)</h4>
               <p>表示OJ内部出现错误。<br>
                由于我们的OJ可能存在一些小问题，所以出现这个信息请原谅，同时请及时与管理员、老师联系。</p>
            </div>
        </div>
    </div>
</div>
<div id="faq_3" class="ui black segment">
    <div class="header"><h4>3. 为什么我的程序在VC++/VC下能正常编译，但是在OJ上使用G++/GCC就会出现'Compilation Error'？</h4></div>
    <div class="content">
        GCC/G++和VC/VC++有所不同，例如：<br>
        在G++/GCC下'main'函数必须定义成int型，定义成void main会得到'Compilation Error'。<br>
        在G++/GCC中itoa不是一个标准的ANSI函数。<br>
        GNU C/C++ Compiler环境下，请使用long long替代__int64（或者#define __int64 long long)，使用%lld替代%I64d<br>
        atoi()不是C语言的标准支持函数，在GNU GCC环境下不支持。<br>
        scanf_s 为VS2005以上版本提供的安全输入函数，GNU GCC环境不支持。<br>
    </div>
</div>
<div id="faq_4" class="ui black segment">
    <div class="header"><h4>4. 为什么我登录不了账号？</h4></div>
    <div class="content">
        首先，请检查是否在正确的系统登录。比如：如果你是教学系统的用户，请在教学系统的登录界面登录账号。<br/>
        然后，请检查输入的密码是否正确，是否开启了大写锁定等。如果是使用初始密码登录，建议登录后立即修改密码，并且不要依赖使用教务密码登录。
    </div>
</div>
<div id="faq_5" class="ui black segment">
    <div class="header"><h4>5. 为什么会有这么多个不同的系统又不同的账户，我好混乱啊！</h4></div>
    <div class="content">
        如果您是1.0版本的老用户，首先感谢您对1.0版本的支持！<br />
        是的，从2.0版本开始，WeJudge使用了全新的账户系统。我们对教学系统、比赛系统的账户进行了“物理”隔离，使得它们互不干涉，
        各自完成自己的工作。<br />
        当然，账号多了，要记也麻烦；并且也会有单纯来刷题的人也要使用系统。因此，我们采用了“主账户+子账户”的模型，也就是
        “WeJudge主账户”，您可以将不同子系统的账户关联到主账户，当您的主账户已登录的时候，进入子系统，将可以看到“一键登录”的选项<br />
        对于在使用习惯上的改变，造成不便敬请原谅。
    </div>
</div>
<div id="faq_6" class="ui black segment">
    <div class="header"><h4>6. 程序怎样取得输入、进行输出?</h4></div>
    <div class="content">
        你的程序应该从标准输入stdin('Standard Input')获取输出，并将结果输出到标准输出stdout('Standard Output')。<br>
        例如，在C语言可以使用 'scanf' ，在C++可以使用'cin' 进行输入；在C使用 'printf' ，在C++使用'cout'进行输出。<br><br>
        下面是“A+B”问题的标准代码：<br>
        <h5>C语言</h5>
            <pre class="ui secondary segment">#include &lt;stdio.h&gt;
int main(){
int a,b;
while(scanf("%d %d",&amp;a, &amp;b) != EOF){
    printf("%d\n",a+b);
}
return 0;
}</pre>
            <h5>C++</h5>
                    <pre class="ui secondary segment">#include &lt;iostream&gt;
using namespace std;
int main(){
int a,b;
while(cin &gt;&gt; a &gt;&gt; b){
    cout &lt;&lt; a+b &lt;&lt; endl;
}
return 0;
}</pre>
            <h5>Java</h5>
                    <pre class="ui secondary segment">import java.util.Scanner;
public class Main {
public static void main(String[] args){
    Scanner scan = new Scanner(System.in);
    while(scan.hasNext()){
        int a = scan.nextInt();
        int b = scan.nextInt();
        System.out.println(String.format("%d", a + b));
    }
}
}</pre>
    </div>
    <div id="faq_7" class="ui black segment">
    <div class="header"><h4>7. 关于OJ的上传图片、文件等功能的限制是什么样的？</h4></div>
    <div class="content">
        【CKEditor编辑器图片上传】<br />
        允许的文件格式：JPG、PNG、BMP、GIF<br />
        最大允许上传：5MB<br />
        【CKEditor编辑器文件上传】<br />
        允许的文件格式：DOC、PPT、XLS、PDF、ZIP、GZ、TXT、JPG、PNG、BMP、GIF<br />
        最大允许上传：20MB<br />
        【教学资源仓库】<br />
        最大允许上传：1000MB<br />
        【测试数据】<br />
        最大允许上传：100MB<br />
        【用户头像】<br />
        允许的文件格式：JPG、PNG、BMP、GIF<br />
        最大允许上传：2MB<br />
        <br >
        未说明的，默认最大可以上传1MB文件，不限制格式。导入数据用的模板如果不是XLS格式会报错。
    </div>
</div>
</div>
# Api自动化测试

#### 介绍
Api接口自动化测试，编辑Excle就可实现的接口自动化测试框架

https://www.processon.com/view/link/6580017d4c36e55bf120b1dd

#### 软件架构
软件架构说明


#### 安装教程

1.  xxxx
2.  xxxx
3.  xxxx

#### 使用说明

**一、比对具体字段怎么解决**
使用jsonpath库，用法：

示例参考：
1. 基本语法：
  
    <font color = red>`$`</font> ：根节点，也是所有JsonPath表达式的开始
  
    <font color = red>`.`</font> ：当前节点

    <font color = red>`..` </font>：递归下级节点

2. 属性操作：

    <font color = red>`$.property` </font>：选择指定属性

    <font color = red>`$['property']` </font>：选择指定属性，属性名带有特殊字符时使用

3.  数组操作：

   <font color = red>`$.array[index]` </font>：选择指定索引处的元素

   <font color = red>`$.array[start:end]`</font> ：选择指定范围内的元素

4. 过滤器：

   <font color = red>`$.array[?(@.property == value)]`</font> ：根据条件过滤数组元素

   <font color = red>`$.array[?(@.property > value)]`</font> ：根据条件过滤数组元素

5. 路径组合：

   <font color = red>`$.parent.child`</font> ：选择父节点下的子节点

   <font color = red>`$.parent[*].child` </font>：选择父节点下所有子节点的某个属性

**参考以上的JSON**

```python
# 获取根目录下的子字段：获取用户名
$.name
# 获取根目录下的字典中的数据：获取地址中的城市（"country": "USA"）
$.address.country
# 获取根目录下的列表中的某个数据：获取教育经历
$.education[0]
# 获取根目录下的列表中的所有数据中的某个字段：获取教育经历中的年
$.education[0:].year
# 获取根目录下的列表中满足某个条件的数据：获取教育经历中的年等于2020 的数据，== \！=
$.education[?(@.year==2020)]
# 获取所有的数据
$.*
```

在线解析 **http://www.atoolbox.net/Tool.php?Id=792**

```python
import jsonpath
# 注意：
# 1. jsonpath处理的数据必须是字典格式
# 2. 报文的格式是json，必须进行数据的转换。
# 3. json.loads() 将json转换成字典类型
res = jsonpath.jsonpath(data,"$.name")
print(res)
```



#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)

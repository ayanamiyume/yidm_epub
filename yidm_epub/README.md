把资源解压后移动到src文件夹下（若没有src需要自己创建）

src目录结构如下：

images:{

    bookimgs:{
    ...
    }

    inbetweenings:{
        ...
    }

    }

novels:{
    ...
}

inbetweening.json

menu.json

volumes.json


运行run.py只能生成一本epub，若要批量操作，需要另写脚本添加进程或循环

经过实际运行发现会越来越慢，因为每次都是从bookid=1开始循环，随着制作数量的增加，多余的循环也会增加，明显降低速度；
可以另写脚本运行此脚本，通过动态修改脚本的方法提速。

我在实际运行中使用了runme.py脚本，采用了五个进程，但此脚本可以优化，如上述的动态修改run.py中的起始bookid
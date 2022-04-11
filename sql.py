# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : sql.py
# Time       ：2022/4/6 16:02
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7
# Description：all the used sql
"""

'''
id ID, enable 是否可用, subject 报告名称, object 对象名称, method 实验方法,
researcher 实验人员, create_time 创建时间, modify_time 更新时间, purpose 实验目的,
principle 实验原理, equipment 实验材料, step 实验步骤, result 结果, discussion 讨论. 
'''
sql_create_table = '''create table if not exists record
                        (ID integer primary key autoincrement,
                        enable boolean default 1,
                        subject text not null,
                        object text not null,
                        method text not null,
                        researcher text not null,
                        create_time TimeStamp default (datetime('now','localtime')),
                        modify_time TimeStamp default (datetime('now','localtime')),
                        purpose text,
                        principle text,
                        equipment text,
                        step text,
                        result text,
                        discussion text)'''

sql_insert_example = '''insert into record(subject, object, method, researcher, purpose, principle, equipment, step, 
                        result, discussion) values ('生长曲线实验示例', 'E.coli', '比浊法', '改自豆丁网示例', 
                        '1.练习无菌操作技术，学习液体培养基配制和接种方法；\n2.掌握利用细菌悬液浑浊度间接测定细菌生长的方法；\n3.了解细菌生长曲线特征，测定细菌繁殖代时。',
                        '    将一定量的菌种接种在液体培养基内，在一定的条件下培养，可观察到细菌的生长繁殖存在一定的规律性。如以活菌数的对数作纵坐标，以培养时间作横坐标，可绘成一条曲线，
                        称为生长曲线。单细胞微生物发酵具有4个阶段，即调整期（迟滞期）、对数期（旺盛期）、平衡期（稳定期）、衰亡期（死亡期），生长曲线可表示细菌从开始生长到死亡的全动态过程。
                        不同微生物具有不同的生长曲线，同种微生物在不同培养条件下，其生长曲线也不一样。因此，测定微生物的生长曲线对于了解和掌握微生物的生长规律是很有帮助的。\n
                            测定微生物生长曲线的方法很多，有比浊法、计数法、菌丝测长法、称重法等，本实验采用比浊法。由于细胞悬液的浓度与浑浊度成正比，因此可以利用分光光度计测定菌悬液的光密度来推知菌液的浓度。
                        将测得的光密度（Optical Density, OD）值与对应的培养时间作图，即可绘出该菌在该条件下的生长曲线。注意，由于光密度值表示的是培养液中的总菌数，包括了活菌和死菌，因此生长曲线的衰亡期不明显。\n
                            从生长曲线我们可以算出细胞每分裂一次所需要的时间，即代时，以G表示。t1和t2为所取对数期两点的时间，W1和W2分别为对应时间测得的OD值。计算公式为：\n\tG = (t2-t1)/[(lgW1-lgW2)/lg2]',
                        '    大肠杆菌、牛肉膏蛋白胨葡萄糖培养基、722s分光光度计、培养箱、取液器、无菌吸头、比色皿、参比杯等。',
                        '1.活化\n    将大肠杆菌接种到牛肉膏蛋白胨葡萄糖三角瓶培养基中，37℃振荡培养18h，另外准备单菌落平板1块。\n
                        2.接种\n    按表1接种。\n3.培养测量\n    每培养1h取样一次，取500μl培养液到2000μl蒸馏水中，以蒸馏水为对照，测定OD600，固定参比杯，不要调动波长旋钮。',
                        '1.OD600记录\n    记录结果见表2及图1-6。\n2.代时计算\n    计算结果见表3。',
                        '    从实验结果看出，不同菌种数量、不同菌种状态、不同温度、不同转速等条件下，发酵的生长曲线和代时有很大差异，下面我们讨论菌种数量作为示例。\n
                            我们选用培养瓶1、2、3号绘制生长曲线，见图7。从中可以看出，不同接种数量对生长曲线和代时影响不大。理论上讲接种数量越大，生长越快。
                        可能由于菌种活性问题，导致接种数量提升但是活性没有相应的成正比提高，出现了我们实验中的结果。'
                        ) '''

sql_select_example = '''select * from record where ID = 1'''

sql_select_records = '''select ID, subject, object, method, researcher, create_time from record where enable = 1'''

sql_disable_arecord = '''update record set enable = 0 where ID = ?'''

sql_insert_arecord = '''insert into record(subject, object, method, researcher) values (?, ?, ?, ?)'''

sql_update_arecord = '''update record set modify_time = (datetime('now','localtime')), purpose = ?, principle = ?, 
                          equipment = ?, step = ?, result = ?, discussion = ? where ID = ?'''

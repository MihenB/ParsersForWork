string = 'Кого «обувают» в Новороссийске\n\n\n 28 сентября 2022 г.\n\n Ольга Филимонова\n\n\n\n\n\n\n\nРаботники обувной фабрики в Новороссийске вышли на забастовку. Люди хотят справедливости и пытаются отстоять свои права. Оказывается, им серьезно задерживают зарплату.\nИстория касается компании ООО «ВетАнна» (входит в ГК «Брис-Босфор»), которая занимается производством обуви, и ООО «Бразис-обувь» (занимается оптовой торговлей обувью), сообщает корреспондент\xa0УтроNews.\nКак стало известно\xa0«Коммерсант», люди вышли на несанкционированную забастовку из-за ситуации с зарплатами. Мастер фабрики Марина Николюк говорит, что деньги рабочим не выплачивают с июня, более того, есть люди, которые не получили зарплату за январь-март текущего года. Она добавила, что начальство их постоянно просит потерпеть, подождать. Однако терпение людей лопнуло.\nКто есть кто?\nГендиректором ООО «ВетАнна» является Михаил Хохлов, а учредитель предприятия — Лужина Татьяна Николаевна. В отношении компании было возбуждено 78 исполнительных производств, предприятие участвовало в 59 арбитражных делах: в 7 в качестве истца, и в 44 в качестве ответчика, также говорится на сайте.\nЛужина Татьяна Николаевна есть и среди учредителей ООО «Брис-Босфор» (производство обуви). Руководитель (гендиректор) ООО «Бразис-обувь», согласно данным «Спарк-Интерфакс» — Аникеев Денис Анатольевич, а учредителями указаны Аникеев Денис Анатольевич, Аникеев Анатолий Иванович.\n«Коммерсант» пишет, что сейчас против ООО «Бразис-обувь» по заявлению Фонда промышленности Москвы инициировано банкротное дело, однако суд пока не вынес решение.\nФинансы поют романсы?\nМихаил Хохлов, прибывший на место событий, общаться с бастующими не стал, как и с журналистом «Коммерсанта».\nПо информации издания, проект открытия импортозамещающего производства кожаной обуви «ВетАнна» в Новороссийске несколько лет назад одобрил Минпромторг РФ. Позднее исполнительный директор ООО «ВетАнна» Михаил Хохлов говорил, что инвестиционный проект находится на стадии реализации.\nРаботники фабрики говорят, что с 2017 года в цехах не появилось новое оборудование, ассортимент выпускаемых товаров серьезно сократился, сотрудникам стали задерживать ЗП и переводить их из одной фирму в другую.\nА в минувшем году АС Краснодарского края ввел процедуру наблюдения в отношении ООО «Брис-босфор». Исковое заявление поступило из налоговой инспекции.\nПо информации «Коммерсанта», финансовые проблемы начались в феврале, но не этого, а 2019 года. Все началось после проверки со стороны Центробанка банка «Восточный».\nВ прошлом году администрация Новороссийска подала в отношении ООО «ВетАнна» иск о банкротстве. Проблемы были с задолженностью по арендной плате за земельный участок. А летом этого года сообщалось, что обувной завод в Новороссийске возобновляет работу.\nНо вернемся в наши реалии. Забастовку не оставили без внимания правоохранительные органы. Следственный отдел по Новороссийску областного управления СК РФ организовал доследственную проверку по невыплате зарплаты сотрудникам фабрики.'


def format_text(text):
    text = text.split('\n\n\n\n\n\n\n\n')[1]
    return text
print(format_text(string))




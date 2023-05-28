### отчитываюсь:

В основном с замечаниями справился н оесть нюансы):

-если делаю FollowSerializer на User, то всё рушится, в режиме отладки получаю такие ошибки как:

  Got AttributeError when attempting to get a value for field `username` on serializer `FollowSerializer`.
The serializer field might be named incorrectly and not match any attribute or key on the `Follow` instance.
Original exception text was: 'Follow' object has no attribute 'username',

Got AttributeError when attempting to get a value for field `email` on serializer `FollowSerializer`.
The serializer field might be named incorrectly and not match any attribute or key on the `Follow` instance.
Original exception text was: 'Follow' object has no attribute 'email' и подобные, 

все свеловь к тому что добавлял новые методы типа этого

def get_email(self, obj):
    """Получаем email пользователя"""
    return obj.user.email 

и сериалайзер становился еще больше чем был, поэтому оставил пока как было 


- немного не уловил по поводу class CustomUserAmin(UserAdmin),
пробовал по разному с add_form но разницы не заметил..

- в settings ис параметром дефолт поиграться, тож не уловил, в итоге потом оставлю только постгресс..

- по поводу этого def subscriptions(self, request): и сократить до одной строчки, то пробовал, и вроде потом все работало,
но потом чето пошло не так, и толи я дурак толи хз, но в один момент при ипорте фоллоус_сериалайзер в миксины, не проходил иморт...хотя в других модулях такиех проблем не было, такиже глюки были и при разбитие на много мелких приложений, все пути 10 раз перепроверял...по этому оставил пока рецепты и юзеров..

- по поводу как подружил бек и фронт, то делал все как в каком то из спринтов, то удалил пакадж_лок.жсон, потом npm i,
,подправил сеттингс, подпраил пакадж.жсон, ну и в одном терминале запустил бек, в другом фронт...сейчас когда все проверял также делал, не в контейнерах, это уже будет следующий этап...

вообщем как то так, пиши замечания!

если что я в пачке+)
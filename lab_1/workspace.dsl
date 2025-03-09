workspace {
    name "Мессенджер"
    description "Приложение для отправки сообщений в групповых и приватных чатах"
    !identifiers hierarchical

    model {
        user = person "Пользователь" {
            description "Пользователь мессенджера"
        }
        messenger = softwareSystem "Мессенджер" 

        user_context = softwareSystem "Область пользователей" {
            description "Управление пользователями мессенджера"

            auth_service = container "Сервис авторизации" {
                description "Управляет авторизацией пользователей"
                technology "HTTP"
            }

            user -> auth_service "Запрашивает авторизацию"
        }

        chat_context = softwareSystem "Чат-область" {
            description "Управление личными (PtP) и групповыми чатами"

            ptp_chat = container "PtP Чат" {
                description "Личный чат между двумя пользователями"
                technology "WebSocket"
            }

            group_chat = container "Групповой чат" {
                description "Чат из нескольких пользователей"
                technology "WebSocket"
            }

            message_service = container "Сервис обработки сообщений" {
                description "Управляет сохранением и получением сообщений"
                technology "HTTP"
            }

            message_storage = container "Хранилище сообщений" {
                description "Управляет сохранением и получением сообщений"
                technology "MongoDB"
            }

            user_context -> group_chat "Даёт доступ пользователю к"
            user_context -> ptp_chat "Даёт доступ пользователю к"
            user -> group_chat "Участвует в"
            user -> ptp_chat "Участвует в"
            group_chat -> message_service "Сохраняет сообщение в"
            ptp_chat -> message_service "Сохраняет сообщение в"
            message_service -> message_storage "Помещает сообщение в"
            message_storage -> message_service "Получает сообщение из"
            message_service -> group_chat "Запрашивает сообщения из"
            message_service -> ptp_chat "Запрашивает сообщения из"
            chat_context -> user "Получает сообщения из"
        }

        notification_context = softwareSystem "Уведомления" {
            description "Обработка уведомлений о непрочитанных сообщениях"

            notification_service = container "Сервис уведомлений" {
                description "Отправляет уведомления пользователям о непрочитанных сообщениях"
                technology "HTTP"
            }

            chat_context.message_service -> notification_service "Отправляет информацию о непрочитанных сообщениях"
            notification_service -> user "Получает уведомления от"
        }
    }

    views {
        systemContext user_context {
            include *
            autoLayout
            title "Контекст пользователей"
        }

        container chat_context {
            include *
            autoLayout
            title "Контекст чатов"
        }

        systemContext notification_context {
            include *
            autoLayout
            title "Контекст уведомлений"
        }

        dynamic messenger  {
            description "Сценарий отправки PtP сообщения"
            autoLayout

            user -> user_context.auth_service "1. Запрашивает авторизацию"
            user_context.auth_service -> user "2. Возвращает токен авторизации"
            user -> chat_context.ptp_chat "3. Отправляет сообщение в"
            chat_context.ptp_chat -> chat_context.message_service "4. Создаёт PtP сообщение"
            chat_context.message_service -> chat_context.message_storage "5. Сохраняет сообщение"
            chat_context.message_service -> notification_context.notification_service "6. Отправляет информацию о новом сообщении"
            notification_context.notification_service -> user "7. Отправляет уведомление о непрочитанном сообщении"
        }

        styles {
            element "SoftwareSystem" {
                background #788B9F
                color #ffffff
            }

            element "Container" {
                background #85F09C
                color #000000
            }

            element "Person" {
                shape Person
                background #B7600E
                color #ffffff
            }

            element "Dynamic" {
                background #EA8DF5
                color #000000
            }
        }
    }
}
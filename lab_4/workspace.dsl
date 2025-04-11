workspace {
    name "Мессенджер"
    description "Приложение для отправки сообщений в групповых и приватных чатах"
    !identifiers hierarchical

    model {
        user = person "Пользователь" {
            description "Пользователь мессенджера"
        }

        messenger = softwareSystem "Мессенджер" {
            description "Управление пользователями и чатами (личными (PtP) и групповыми)"

            user_db = container "База данных пользователей" {
                description "Хранит данные пользователей"
                technology "PostgreSQL"
            }

            user_service = container "Сервис обработки пользователей" {
                description "Обрабатывает запросы, связанные с пользователями" 
                technology "Python/FastAPI"
            }

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
                technology "Python/FastAPI"
            }

            message_storage = container "Хранилище сообщений" {
                description "Управляет сохранением и получением сообщений"
                technology "MongoDB"
            }

            user -> user_service "Запрашивает авторизацию"
            user -> user_service "Создаёт пользователя и производит поиск пользователей"
            user_service -> user_db "Сохранение информации о пользователе" "JDBC"
            user_db -> user_service "Получение информации о пользователе" "JDBC"

            user_service -> group_chat "Предоставляет доступ пользователю к"
            user_service -> ptp_chat "Предоставляет доступ пользователю к"
            user -> group_chat "Участвует в"
            user -> ptp_chat "Участвует в"
            group_chat -> message_service "Сохраняет сообщение в"
            ptp_chat -> message_service "Сохраняет сообщение в"
            message_service -> message_storage "Помещает сообщение в"
            message_storage -> message_service "Получает сообщение из"
            message_service -> group_chat "Запрашивает сообщения из"
            message_service -> ptp_chat "Запрашивает сообщения из"
            messenger -> user "Получает сообщения из"
        }

        notification_context = softwareSystem "Уведомления" {
            description "Обработка уведомлений о непрочитанных сообщениях"

            notification_service = container "Сервис уведомлений" {
                description "Отправляет уведомления пользователям о непрочитанных сообщениях"
                technology "HTTP"
            }

            messenger.message_service -> notification_service "Отправляет информацию о непрочитанных сообщениях"
            notification_service -> user "Получает уведомления от"
        }
    }

    views {
        systemContext messenger {
            include *
            autoLayout
            title "Контекст мессенджера"
        }

        container messenger {
            include *
            autoLayout
            title "Контейнеры мессенджера"
        }

        systemContext notification_context {
            include *
            autoLayout
            title "Контекст уведомлений"
        }

        dynamic messenger  {
            description "Сценарий отправки PtP сообщения"
            autoLayout

            user -> messenger.user_service "1. Запрашивает авторизацию"
            messenger.user_service -> user "2. Возвращает токен авторизации"
            user -> messenger.ptp_chat "3. Отправляет сообщение в"
            messenger.ptp_chat -> messenger.message_service "4. Создаёт PtP сообщение"
            messenger.message_service -> messenger.message_storage "5. Сохраняет сообщение"
            messenger.message_service -> notification_context.notification_service "6. Отправляет информацию о новом сообщении"
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
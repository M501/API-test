# Antisleep API Automation Python Tests

Cсылка на постман с коллекциями: https://app.getpostman.com/join-team?invite_code=72d033782172be3d22d1d436a429661d209b8dfb9015786e027d1d97910bcc09&target_code=b83c1a9d4ed9cb23cdfd0768d9585c10

# A. Authentication Test Cases
| ID    | Title                          | Preconditions | Steps                                                                                     | Expected Result                                                                                          |
| ----- | ------------------------------ | ------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| TC‑A1 | Login – Success                | API доступен  | 1. POST `/public/login` с `{ "email":"demo@demo.ru", "password":"Demo1704@demo.ru" }`     | 200 OK; в теле есть непустой `token`.                                                                    |
| TC‑A2 | Login – Wrong Password         | API доступен  | 1. POST `/public/login` с `{ "email":"demo@demo.ru", "password":"WrongPass123" }`         | 401 Unauthorized; `message` содержит `"Invalid username or password"`.                                   |
| TC‑A3 | Login – Wrong Email            | API доступен  | 1. POST `/public/login` с `{ "email":"notexist@demo.ru", "password":"Demo1704@demo.ru" }` | 401 Unauthorized; `message` содержит `"Invalid username or password"`.                                   |
| TC‑A4 | Login – Missing Both Fields    | API доступен  | 1. POST `/public/login` с `{ "email":"", "password":"" }`                                 | 422 Unprocessable Entity; `errors.email` содержит сообщение о обязательном поле.                         |
| TC‑A5 | Login – Missing Email Field    | API доступен  | 1. POST `/public/login` с `{ "email":"", "password":"Demo1704@demo.ru" }`                 | 422 Unprocessable Entity; `errors.email` содержит сообщение о обязательном поле.                         |
| TC‑A6 | Login – Missing Password Field | API доступен  | 1. POST `/public/login` с `{ "email":"demo@demo.ru", "password":"" }`                     | 422 Unprocessable Entity; `errors.password` содержит сообщение о обязательном поле.                      |
| TC‑A7 | Login – Email Too Short        | API доступен  | 1. POST `/public/login` с `{ "email":"a@b", "password":"Demo1704@demo.ru" }`              | 401 Unauthorized; `message` содержит `"Invalid username or password"`.                                   |
| TC‑A8 | Login – Email Invalid Format   | API доступен  | 1. POST `/public/login` с `{ "email":"notanemail", "password":"Demo1704@demo.ru" }`       | 422 Unprocessable Entity; `errors.email` содержит сообщение `"The email must be a valid email address"`. |

# B. Update User Settings Test Cases

Если используем Postman, то используем Authorization: Bearer "token from TC-A1".

# Обязательные/необязательные значения для редактирования данных пользователя

Обязательный все, кроме "sip_number", "sip_extension", так же "locale" принимает значения либо "en", либо "ru".

# B.1 Позитивные сценарии

| ID     | Title                                    | Step-Payload                                                                                                                       | Expected Result                                                                           |
| ------ | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| TC‑B1  | Update Settings – Success                | `{"name":"John Doe", "time_zone":"Asia/Yakutsk", "sip_number":"123456", "sip_extension":"7890", "events_view_type":1, "locale":"en"}` | 200 OK; `{ "success": true }`                                                             |
| TC‑B2  | Update Settings – Name Too Long          | `{"name":<long >255 chars>, "time_zone":"Asia/Yakutsk", ...}`                                                                         | 422 Unprocessable Entity; `errors.name` содержит ограничение длины                        |
| TC‑B3  | Update Settings – SIP Number Optional    | `{"name":"John Doe", "time_zone":"Asia/Yakutsk", "events_view_type":1, "locale":"en"}`                                                | 200 OK; `{ "success": true }`                                                             |
| TC‑B4  | Update Settings – SIP Extension Optional | `{"name":"John Doe", "time_zone":"Asia/Yakutsk", "events_view_type":1, "locale":"en"}`                                                | 200 OK; `{ "success": true }`                                                             |
| TC‑B5  | Update Settings – All Optional Fields    | `{"name":"John Doe", "time_zone":"Asia/Yakutsk", "events_view_type":1}`                                                               | 200 OK; `{ "success": true }`                                                             |
| TC‑B6  | Update Settings – Invalid Name Chars     | `{"name":"John@Doe!","time_zone":"Asia/Yakutsk","sip_number":"123456","sip_extension":"7890","events_view_type":1,"locale":"en"}`     | 422 Unprocessable Entity; `errors.name` содержит сообщение о недопустимых символах        |
| TC‑B7  | Update Settings – Invalid Time Zone      | `{"name":"John Doe","time_zone":"Invalid/Zone", ...}`                                                                                 | 422 Unprocessable Entity; `errors.time_zone` содержит сообщение об ошибке формата         |
| TC‑B8  | Update Settings – Missing Locale         | `{"name":"John Doe","time_zone":"Asia/Yakutsk","sip_number":"123456","sip_extension":"7890","events_view_type":1}`                    | 200 OK *или* 422 в зависимости от обязательности; проверить `success` или `errors.locale` |
| TC‑B9  | Update Settings – Name with Spaces       | `{"name":" John Doe ", ...}`                                                                                                          | 200 OK; `{ "success": true }`                                                             |
| TC‑B10 | Update Settings – Time Zone with Spaces  | `{"time_zone":" Asia/Yakutsk ", ...}`                                                                                                 | 200 OK; `{ "success": true }`                                                             |
| TC‑B11 | Update Settings – Locale with Spaces     | `{"locale":" en ", ...}`                                                                                                              | 200 OK; `{ "success": true }`                                                             |
| TC‑B12 | Update Settings – Invalid SIP Number     | `{"sip_number":"123@456", ...}`                                                                                                       | 422 Unprocessable Entity; `errors.sip_number` содержит сообщение об ошибке                |
| TC‑B13 | Update Settings – Invalid SIP Extension  | `{"sip_extension":"789@0", ...}`                                                                                                      | 422 Unprocessable Entity; `errors.sip_extension` содержит сообщение об ошибке             |

# B.2 Негативные сценарии

| ID     | Title                                  |  Step-Payload                                                                                                        | Expected Result                                                           |
| ------ | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| TC‑B14 | Update Settings – Missing Name         | `{ "time_zone":"Asia/Yakutsk", "sip_number":"123456", "sip_extension":"7890", "events_view_type":1, "locale":"en" }` | 422; `errors.name` содержит сообщение о поле name                         |
| TC‑B15 | Update Settings – Name Too Short       | `{ "name":"", "time_zone":"Asia/Yakutsk", ... }`                                                                     | 422; `errors.name` содержит сообщение о пустом поле                       |
| TC‑B16 | Update Settings – Non‑Latin Name       | `{ "name":"漢字テスト", "time_zone":"Asia/Yakutsk", "events_view_type":2, "locale":"fr"}`                                 | 422 *или* 200; уточнить политику; проверить `errors.name` или `success`   |
| TC‑B17 | Update Settings – Missing Events View  | `{ "name":"John Doe","time_zone":"Asia/Yakutsk","sip_number":"123456","sip_extension":"7890","locale":"en"}`         | 422; `errors.events_view_type` содержит сообщение о поле                  |
| TC‑B18 | Update Settings – Invalid Events View  | `{ "events_view_type":3, ...}`                                                                                       | 422; `errors.events_view_type` содержит сообщение о недопустимом значении |
| TC‑B19 | Update Settings – Invalid Locale Value | `{ "locale":"xx", ...}`                                                                                              | 422; `errors.locale` содержит сообщение о недопустимом значении           |


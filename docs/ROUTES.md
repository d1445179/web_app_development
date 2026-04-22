# 路由設計文件 (API Design)

本文件依據流程圖與架構設計，定義待辦事項系統中所有的 URL 路由、HTTP 方法及對應的處理邏輯與 Jinja2 模板。

## 1. 路由總覽表格

| 功能名稱 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁與任務列表 | `GET` | `/` | `index.html` | 查詢並顯示所有任務 |
| 新增任務 | `POST` | `/add` | — | 接收表單內容並建立新任務，完成後重導向 `/` |
| 檢視編輯介面 | `GET` | `/edit/<int:task_id>` | `edit.html` | 顯示單一任務的編輯表單畫面 |
| 儲存編輯內容 | `POST` | `/edit/<int:task_id>` | — | 儲存修改過後的單一任務內容，完成後重導向 `/` |
| 標記任務狀態 | `POST` | `/complete/<int:task_id>`| — | 切換單一任務為已完成（或未完成）狀態，完成後重導向 `/` |
| 刪除任務 | `POST` | `/delete/<int:task_id>` | — | 從系統中永久移除單一任務，完成後重導向 `/` |

## 2. 每個路由的詳細說明

### 首頁與任務列表
- **路徑**：`GET /`
- **輸入**：無
- **處理邏輯**：呼叫 `TaskModel.get_all_tasks()` 取得所有任務資料。
- **輸出**：渲染 `index.html`，並將任務資料傳入模板中。
- **錯誤處理**：若無資料，前端模板應顯示「目前尚無任務」。

### 新增任務
- **路徑**：`POST /add`
- **輸入**：表單欄位 `title` (必填), `description` (選填)
- **處理邏輯**：
  1. 驗證 `title` 是否存在。
  2. 呼叫 `TaskModel.create_task(title, description)` 寫入資料庫。
- **輸出**：重導向至 `/`。
- **錯誤處理**：若 `title` 驗證失敗，應回傳錯誤訊息或重導向回首頁。

### 檢視編輯介面
- **路徑**：`GET /edit/<int:task_id>`
- **輸入**：URL 參數 `task_id`
- **處理邏輯**：呼叫 `TaskModel.get_task_by_id(task_id)` 取得指定任務資料。
- **輸出**：渲染 `edit.html`，將取得的任務資料傳入以便在表單中呈現預設值。
- **錯誤處理**：若找不到該 `task_id` 的任務，回傳 404 錯誤頁面或重導向至 `/`。

### 儲存編輯內容
- **路徑**：`POST /edit/<int:task_id>`
- **輸入**：URL 參數 `task_id`，表單欄位 `title` (必填), `description` (選填)
- **處理邏輯**：呼叫 `TaskModel.update_task(task_id, title, description)`。
- **輸出**：重導向至 `/`。
- **錯誤處理**：若 `title` 驗證失敗，保留在編輯頁面並顯示錯誤訊息。若任務不存在，回傳 404。

### 標記任務狀態
- **路徑**：`POST /complete/<int:task_id>`
- **輸入**：URL 參數 `task_id`
- **處理邏輯**：呼叫 `TaskModel.toggle_task_status(task_id)` 切換該任務的完成狀態（0 <-> 1）。
- **輸出**：重導向至 `/`。
- **錯誤處理**：若任務不存在，回傳 404 錯誤頁面或重導向至 `/`。

### 刪除任務
- **路徑**：`POST /delete/<int:task_id>`
- **輸入**：URL 參數 `task_id`
- **處理邏輯**：呼叫 `TaskModel.delete_task(task_id)` 刪除該任務。
- **輸出**：重導向至 `/`。
- **錯誤處理**：若任務不存在，忽略並重導向至 `/`。

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 目錄下：

1. **`base.html`**
   - 網站基本骨架，包含 HTML `<head>` 宣告、共用的 CSS (`style.css`) 與 JavaScript 引入。
2. **`index.html`**
   - 繼承自 `base.html`。
   - 包含新增任務表單，以及分為「進行中」與「已完成」的任務列表。
3. **`edit.html`**
   - 繼承自 `base.html`。
   - 顯示可修改任務名稱與備註的表單。

## 4. 路由骨架程式碼
請參考 `app/routes/task_routes.py`。

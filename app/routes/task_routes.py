from flask import Blueprint, render_template, request, redirect, url_for

# 建立 Blueprint 以模組化管理路由
task_bp = Blueprint('tasks', __name__)

@task_bp.route('/', methods=['GET'])
def index():
    """顯示首頁與所有任務列表"""
    pass

@task_bp.route('/add', methods=['POST'])
def add_task():
    """接收表單，新增任務並重導向首頁"""
    pass

@task_bp.route('/edit/<int:task_id>', methods=['GET'])
def edit_task_page(task_id):
    """顯示單一任務的編輯表單畫面"""
    pass

@task_bp.route('/edit/<int:task_id>', methods=['POST'])
def update_task(task_id):
    """儲存修改過後的單一任務內容，完成後重導向首頁"""
    pass

@task_bp.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    """切換單一任務的完成狀態，完成後重導向首頁"""
    pass

@task_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """從系統中永久移除單一任務，完成後重導向首頁"""
    pass

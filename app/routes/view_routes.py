from flask import Blueprint, render_template, redirect, request, url_for, current_app

view_bp = Blueprint("view", __name__)

@view_bp.route('/view')
def view():
    return redirect(url_for('view.view_with_params', page=1, created_at=-1))

@view_bp.route('/view/<int:page>')
def view_with_params(page: int):
    row_in_one_page_limit = current_app.config['ROW_IN_ONE_PAGE_LIMIT']
    database = current_app.config['DATABASE']

    sort_data = []
    sort_args = ['word, isFromBeggining', 'counts', 'hashType', 'user', 'created_at']
    
    for arg in sort_args:
        temp = request.args.get(arg, '0')
        if temp == '1':
            sort_data.append((arg, 1))
        elif temp == '-1':
            sort_data.append((arg, -1))

    if sort_data:
        result = database.find(
            query={},
            sort=sort_data,
            skip=row_in_one_page_limit*(page-1),
            limit=row_in_one_page_limit
        )
    count = database.count()

    return render_template('view.html', result=result, count=count, start_count=int((page-1)*row_in_one_page_limit)+1)
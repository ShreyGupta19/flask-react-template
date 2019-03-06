import React from "react";
import * as strings from '../strings';
import styles from '../../sass/index.scss';

export default class List extends React.Component {
  markStatus (todoId) {
    let data = {id: todoId};  

    fetch('/todos/done', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      },
    }).then((res) => {
      if (!res.ok) throw Error(strings.TODO_DONE_ERR);
      else this.props.toggleStatus(todoId);
    }).catch((error) => this.props.addError(error))
  }

  render () {
    return (
      <div className={styles.list}>
        <ul>
          {this.props.todos.map((todo) =>
            <li key={todo.id}>
              <input 
                type="checkbox"
                checked={todo.done} 
                onChange={() => this.markStatus(todo.id)} />
              {todo.text}
            </li>
          )}
        </ul>
      </div>
    );
  }
}
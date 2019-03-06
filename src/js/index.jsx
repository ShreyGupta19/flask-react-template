import React from "react";
import ReactDOM from "react-dom";
import Form from "./components/form"
import List from "./components/list"
import 'bootstrap';
import styles from '../sass/index.scss';

class TodoApp extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      todos: [],
      errors: [],
    }

    this.addError = this.addError.bind(this);
    this.addTodo = this.addTodo.bind(this);
    this.toggleStatus = this.toggleStatus.bind(this);
  }

  addError (error) {
    this.setState({
      errors: this.state.errors.concat(error.message),
    });
  }

  addTodo (todo) {
    this.setState({
      todos: this.state.todos.concat(todo),
    });
  }

  toggleStatus (todoId) {
    let updatedTodos = this.state.todos;
    let todo = updatedTodos.find((e) => e.id === todoId);
    todo.done = !todo.done
    this.setState({todos: updatedTodos});
  }

  componentDidMount () {
    fetch('/todos', {
      method: 'GET',
    }).then((res) => {
      if (!res.ok) throw Error(strings.TODO_READ_ERR);
      else res.json().then((body) => this.setState({
        todos: body.data,
      }));
    }).catch(this.addError);
  }

  render () {
    return (
      <div className={styles.app}>
        <h1>To-Do List</h1>
        <ul className={styles.errorList}>
          {this.state.errors.map((error, idx) => 
            <li key={idx}>{error}</li>
          )}
        </ul>
        <List
          todos={this.state.todos}
          toggleStatus={this.toggleStatus}
          addError={this.addError}
        />
        <Form
          addTodo={this.addTodo}
          addError={this.addError}
        />
      </div>
    );
  }
}

ReactDOM.render(<TodoApp />, document.getElementById("content"));

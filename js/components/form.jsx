import React from "react";
import * as strings from '../strings';
import sty from '../../sass/main.scss';

export default class Form extends React.Component {
  constructor (props) {
    super(props);
    this.formRef = React.createRef();
  }

  handleSubmit (event) {
    event.preventDefault();
    let formData = new FormData(event.target);
    let objData = {}
    formData.forEach(function(value, key){
      objData[key] = value;
    });
    let jsonData = JSON.stringify(objData);
    fetch('/todos', {
      method: 'POST',
      body: jsonData,
      headers: {
        'Content-Type': 'application/json'
      },
    }).then((res) => {
      if (!res.ok) throw Error(strings.TODO_WRITE_ERR);
      else res.json().then((body) => {
        this.formRef.current.reset();
        this.props.addTodo(body.data);
      });
    }).catch((error) => this.props.addError(error));
  }

  render () {
    return (
      <div className={sty.addForm}>
        <form
          onSubmit={this.handleSubmit.bind(this)}
          ref={this.formRef}
          className={sty.formInline}
        >
          <div className={sty.colLg12}>
            <div className={[sty.inputGroup, sty.inputGroupLg].join(' ')}>
              <input
                type="text"
                className={[sty.formControl, sty.inputLg].join(' ')}
                name="todo"
                placeholder="New todo here!"
              />
              <span className={sty.inputGroupBtn}>
                <button 
                  type="submit" 
                  className={[sty.btn, sty.btnDefault, sty.btnLg].join(' ')}
                >+</button>
              </span>
            </div>
          </div>
        </form>
      </div>
    );
  }
}
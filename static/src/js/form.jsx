import React from 'react';
import ReactDOM from 'react-dom';


const file_fields = [...document.querySelectorAll('.file-group')];

class FileUploader extends React.Component {

  constructor() {
    super();
    this.state = {
      currentFile: null,
      toClear: false
    }

    this.handleUpload = this.handleUpload.bind(this);
    this.handleClear = this.handleClear.bind(this);
    this.getFileStats = this.getFileStats.bind(this);
  }

  handleUpload(uploadEvent) {
    const file = uploadEvent.target.files[0];

    this.setState({
      currentFile: file
    })
  }

  handleClear() {
    this.setState(prevState => {
      toClear: !prevState.toClear
    })
  }

  getFileStats() {
    if (this.state.currentFile !== null) {
      return (
        <div className="file-uploader__stats">
          <span className="file-name">{this.state.currentFile.name}, </span>
          <span className="file-size">{this.state.currentFile.size}</span>
        </div>
      )
    } else if (this.props.inputFile !== null) {
      return (
        <div className="file-uploader__stats">
          <span className="file-name">{this.props.inputFile.textContent}, </span>
        </div>
      )
    } else {
      return (
        <div className="file-uploader__stats">
          <span className="file-name">No file selected.</span>
        </div>
      )
    }
  }

  render() {
    this.props.input.remove();

    const fileStats = this.getFileStats();
    let fileClear = '';

    if (this.props.inputClear) {
      fileClear = <label for={this.props.inputClear.is} onChange={this.handleClear}></label>
    }

    return(
      <div>
        <input
          type="file"
          className="sr__input"
          name={this.props.input.name}
          id={this.props.input.id}
          onChange={this.handleUpload}/>
        <div className="file-uploader">
          <label htmlFor={this.props.input.id} className="button input">
            Pick a file
          </label>
          {fileStats}
        </div>
        {fileClear}
      </div>
    )
  }
}

file_fields.map(field => {
  const mountPoint = field.querySelector('.file-mount');
  const input = field.querySelector('input[type=file]');
  const inputClear = field.querySelector('input[type=checkbox]');
  const inputFile = field.querySelector('a');

  ReactDOM.render(
    <FileUploader
      input={input}
      inputFile={inputFile}
      inputClear={inputClear}
      />,
    mountPoint
  )
});


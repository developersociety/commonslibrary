import React from 'react';
import ReactDOM from 'react-dom';

const file_fields = [...document.querySelectorAll('.file-group')];

class FileUploader extends React.Component {
    constructor() {
        super();
        this.state = {
            currentFile: null
        };

        this.handleUpload = this.handleUpload.bind(this);
        this.getFileStats = this.getFileStats.bind(this);
    }

    handleUpload(uploadEvent) {
        const file = uploadEvent.target.files[0];

        this.setState({
            currentFile: file
        });
    }

    getFileStats() {
        if (this.state.currentFile !== null) {
            return (
                <div className="file-uploader__stats">
                    <span className="file-name">{this.state.currentFile.name}, </span>
                    <span className="file-size">
                        {Math.floor(this.state.currentFile.size / 1024)}kb
                    </span>
                </div>
            );
        }
        if (this.props.inputFile !== null) {
            return (
                <div className="file-uploader__stats">
                    <span className="file-name">{this.props.inputFile.textContent}, </span>
                </div>
            );
        }
        return (
            <div className="file-uploader__stats">
                <span className="file-name">No file selected.</span>
            </div>
        );
    }

    render() {
        // remove initial DOM node
        this.props.inputHolder.remove();

        const fileStats = this.getFileStats();
        let fileClearLabel = '';
        let fileClearField = '';

        if (this.props.inputClear) {
            fileClearLabel = <label htmlFor={this.props.inputClear.id}>Clear</label>;
            fileClearField = (
                <input
                    type="checkbox"
                    className="sr__input"
                    id={this.props.inputClear.id}
                    name={this.props.inputClear.name}
                    onChange={this.handleClear}
                />
            );
        }

        return (
            <div>
                <label htmlFor={this.props.input.id} className="control-label">
                    {this.props.label}
                </label>
                {fileClearField}
                <input
                    type="file"
                    className="sr__input"
                    name={this.props.input.name}
                    id={this.props.input.id}
                    onChange={this.handleUpload}
                />
                <div className="file-uploader">
                    <label htmlFor={this.props.input.id} className="button input">
                        Pick a file
                    </label>
                    {fileStats}
                </div>
                {fileClearLabel}
            </div>
        );
    }
}

file_fields.map((field) => {
    const mountPoint = field.querySelector('.file-mount');
    const label = field.querySelector('.control-label').textContent;
    const input = field.querySelector('input[type=file]');
    const inputHolder = field.querySelector('.control-group');
    const inputClear = field.querySelector('input[type=checkbox]');
    const inputFile = field.querySelector('a');

    ReactDOM.render(
        <FileUploader
            input={input}
            label={label}
            inputHolder={inputHolder}
            inputFile={inputFile}
            inputClear={inputClear}
        />,
        mountPoint
    );
});

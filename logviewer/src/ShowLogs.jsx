import React, { Component } from 'react';
import './App.css';

class ShowLogs extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: {}
        }
    }
    handleHTTPErrors(response) {
        if (!response.ok) throw Error(response.status + ': ' + response.statusText);
        return response;
    }
    componentDidMount() {
        fetch('http://localhost:3004/logs')
            .then(response=> this.handleHTTPErrors(response))
            .then(response=> response.json())
            .then(result=> {
                this.setState({
                    data: result
                });
            })
            .catch(error=> {
                console.log('Fetch API Error: ' + error);
            });
    }
    render () {
        console.log(this.state.data);
        return (<div>
            <h1>Complete</h1>
            {this.state.data.map(category =>
                <p>{category}</p>
            )}</div>);
    }
}


export default ShowLogs;

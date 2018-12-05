import React, { Component } from 'react';
//import ShowTemp from './ShowTemp'
import ShowUFWBlocks from './ShowUFWBlocks'
//import ShowLogs from "./ShowLogs";

const ShowSys = (props) => {
    return (
        <div>
        <table>
            <tr>
                <td>Hostname</td>
                <td>{props.hostname}</td>
            </tr>
            <tr>
                <td>Battery</td>
                <td>{props.battery}</td>
            </tr>
            <tr>
                <td>Temp</td>
                <td>{props.temp}</td>
            </tr>
            <tr>
                <td>Total UFW Blocks</td>
                <td>{props.totalblocks}</td>
            </tr>
        </table>
        </div>
    );
}

class Main extends Component {
    constructor(props) {
        super(props)
        this.state = {
            sys: {},
            ufw: {}
        }
    }
    handleHTTPErrors(response) {
        if (!response.ok) throw Error(response.status + ': ' + response.statusText);
        return response;
    }
    componentDidMount() {
        fetch('http://localhost:3004/sys')
            .then(response=> this.handleHTTPErrors(response))
            .then(response=> response.json())
            .then(result=> {
                this.setState({
                    sys: result
                });
            })
            .catch(error=> {
                console.log('Fetch API Error: ' + error);
            });
        fetch('http://localhost:3004/ufw')
            .then(response=> this.handleHTTPErrors(response))
            .then(response=> response.json())
            .then(result=> {
                this.setState({
                    ufw: result
                });
            })
            .catch(error=> {
                console.log('Fetch API Error: ' + error);
            });
    }
    render () {
            return (
                <div class='main'>
                    <h1>Sekhnet Security Dashboard</h1>
                    <ShowSys { ... this.state.sys}/>
                    <br/>
                    <ShowUFWBlocks { ... this.state.ufw}/>
                </div>
            );

    }
}

export default Main;

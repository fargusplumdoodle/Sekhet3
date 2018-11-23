import React, { Component } from 'react';
import Collapse from './Collapse.js';
import './App.css';

class ShowUFWBlocks extends Component {
    constructor(props){
        super(props);
        this.showInfo = this.showInfo.bind(this);
        this.state = {
            showSrc: false,
        }


    }
    showInfo (event) {
        event.preventDefault();
        console.log(event.currentTarget.id);
        this.setState({
            showSrc: true,
            display: event.currentTarget.id
        });
    }
    render () {
        console.log(this.props);
        if (this.state.showSrc) {
            return (
                <div>
                    <ShowInfo isOpened={this.state.showSrc}/>
                    <table>
                        <th>Time</th>
                        <th>Source</th>
                        {Object.keys(this.props).map(src =>
                            <tr id={src} onClick={this.showInfo}>
                                <td>{src}</td>
                                <td>{this.props[src].freq}</td>
                            </tr>
                        )}
                    </table>
                </div>
            );
        } else {
            return (
                <div>
                    <table>
                        <th>Time</th>
                        <th>Source</th>
                        {Object.keys(this.props).map(src =>
                            <tr id={src} onClick={this.showInfo}>
                                <td>{src}</td>
                                <td>{this.props[src].freq}</td>
                            </tr>
                        )}
                    </table>
                </div>
            );
        }
    }
}

class ShowInfo extends React.PureComponent {
    constructor(props) {
        super(props);
    }
    render () {

        return (
            <div>
                <Collapse isOpened={this.props.isOpened} hasNestedCollapse={true}>
                    <p>this is info</p>
                </Collapse>
            </div>
        );
    }
}


export default ShowUFWBlocks;
/*



                {this.props["Temp"].map( thing =>
					<p>{thing}</p>

				)}
 */

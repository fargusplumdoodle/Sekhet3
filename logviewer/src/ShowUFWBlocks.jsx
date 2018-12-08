import React, { Component } from 'react';
import { Collapse } from 'react-collapse';
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
                    <ShowInfo isOpened={this.state.showSrc} display={this.state.display} info={this.props[this.state.display]}/>
                    <h4 onClick={() =>
                        this.setState({showSrc: false})
                    }>Close</h4>
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
                        <th>Source</th>
                        <th>Number of Blocks</th>
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
        this.state = {
            isOpened: this.props.isOpened
        }
    }
    render () {
        console.log(this.props.info);
        return (
            <div class="showinfo">
                <Collapse isOpened={this.state.isOpened} hasNestedCollapse={true}>
                    <h1>{this.props.display}</h1>
                    <h4>Frequency: {this.props.info.freq}</h4>
                    <div class='log'>
                    <table >
                        <th>Time</th>
                        <th>Port</th>
                        {this.props.info.times.map(time =>
                            <tr>
                                <td>{time}</td>
                                <td>{this.props.info.port}</td>
                            </tr>
                        )}
                    </table>
                    </div>
                </Collapse>
                <br/>
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

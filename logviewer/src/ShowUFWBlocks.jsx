import React, { Component } from 'react';
import './App.css';

class ShowUFWBlocks extends Component {
    constructor(props){
        super(props);
        this.showInfo = this.showInfo.bind(this);

    }
    showInfo (event) {
        console.log('got user click!');
        console.log('got user click!');
        console.log('got user click!');
        console.log('got user click!');
        console.log('got user click!');
        console.log('got user click!');
        console.log('got user click!');
    }
    render () {
        console.log(this.props);
	    return(
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


export default ShowUFWBlocks;
/*



                {this.props["Temp"].map( thing =>
					<p>{thing}</p>

				)}
 */

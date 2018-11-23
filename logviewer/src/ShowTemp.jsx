import React, { Component } from 'react';
import './App.css';

class ShowTemp extends Component {
    render () {
		delete this.props["UFW BLOCK SUM"][0]['type'];

	    return(
		    <div>
                <table id='temp'>
                    <tr>
                        <td>Current Temperature</td>
                        <td>{this.props["Temp"][0]['temp']} </td>
                    </tr>
				</table>
			<br/>
				<table id='temp'>
					<th>Source</th>
                    <th>Frequency</th>
					{Object.keys((this.props["UFW BLOCK SUM"][0])).map(thing =>
						<tr>
                        <td>{thing}</td>
						<td id={thing}>{this.props["UFW BLOCK SUM"][0][thing]}</td>
						</tr>
					)}
				</table>
			<br/>
		    </div>
	    );
    }
}


export default ShowTemp;
/*
                    {this.props["UFW BLOCK SUM"].keys().map(thing =>
                        <td>{thing}</td>
					)}



                {this.props["Temp"].map( thing =>

				)}
 */

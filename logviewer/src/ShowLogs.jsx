import React, { Component } from 'react';
import './App.css';
import ShowUFWBlocks from './ShowUFWBlocks';
import ShowTemp from './ShowTemp'

class ShowLogs extends Component {
    constructor(props) {
        super(props);
        this.state = {
    	    show: false,
            showLogs: false,
        }
    }
    render () {
	    if (this.state.show) {
        	return (
			<div>
                <ShowTemp { ... this.state.data}/>
                <ShowUFWBlocks { ... this.state.data}/>
			</div>);
	    } else {
		    return( 
            <h1>Did not get data</h1>
		    );
	    }
    }
}


export default ShowLogs;

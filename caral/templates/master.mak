<%def name="title()">
    Default Title
</%def>

<!doctype html>
<html>
  <head>
    <title>Pypi :: ${self.title()}</title>
    
    <style type="text/css">
      body  {
        padding: 15px;
        font-family: Helvetica, sans-serif;
        font-size: .9em;
      }
      table  {
        margin: 15px 0;
        border-collapse: collapse;
        border-spacing: 0px;
      }
      table th, td  {
        padding: 5px 8px;
      }
      table th  {
        font-weight: bold;
      }
      table tr:first-child th  {
        background: #000;
        color: #FFF;
        border-right: 1px solid #FFF;
      }
      table tr:nth-child(2n+1) td  {
        background: #EEE;
      }
      table tr.cancelled td  {
        background: #FAFAFA !important;
        color: #C3C3C3;
      }
      table tr.succeeded td.status  {
        color: green;
      }      
      table tr.scheduled td.status  {
        color: orange;
      }
      table tr.failed td.status  {
        color: red;
      }
    </style>
    
  </head>
  <body>
    ${self.body()}
  </body>
</html>

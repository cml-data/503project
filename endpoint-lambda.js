exports.handler = async (event) => {
    const dbData = await dbOps();
    const response = {
      statusCode: 200,
      body: JSON.stringify(dbData),
    };
    return response;
  };
  
  async function dbOps() {
    const { Client } = require('pg');
    const client = new Client({
                     user: "postgres",
                     host: "project503.cduiwke4ucsq.us-west-2.rds.amazonaws.com",
                     database: "postgres",
                     password: "unsecurepwd1!",
                     port: 54322,
                     ssl: true
                   });
    await client.connect();
    const text = 'SELECT * from postgres.public.current_conditions'
   
    const res = await client.query(text)
    // Your other interactions with RDS...
    client.end();
    
    return res.rows
  }
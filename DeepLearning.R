# Libraries
library(keras)
library(mlbench) 
library(dplyr)
library(magrittr)
library(neuralnet)


#import data
AccData <- read.csv("C:/Users/Windows/Dropbox/R-Code/RandomForest/AccData.csv")
data <- AccData

#matrix
data <- as.matrix(data)
dimnames(data) <- NULL

#split into traindata 80%, testdata 20%
set.seed(1234)
ind <- sample(2, nrow(data), replace = T, prob = c(.8, .2))
training <- data[ind==1,1:25]
test <- data[ind==2, 1:25]
trainingtarget <- data[ind==1, 26]
testtarget <- data[ind==2, 26]

# Normalize data
m <- colMeans(training)
s <- apply(training, 2, sd)
training <- scale(training, center = m, scale = s)
test <- scale(test, center = m, scale = s)

# Create initial model
model <- keras_model_sequential()
model %>% 
  layer_dense(units = 50, activation = 'relu', input_shape = c(25)) %>%
  layer_dense(units = 50, activation = 'relu') %>%
  layer_dense(units = 1)

# Compile
model %>% compile(loss = 'mse',
                  optimizer = 'rmsprop',
                  metrics = 'mae')

# run model & see the loss graph
mymodel <- model %>%
  fit(training,
      trainingtarget,
      epochs = 50,
      batch_size = 30,
      validation_split = 0.2)

#improve model process change & run below again

# Create initial model
# Compile
# run model & see the loss graph to improve model

# Performance
model %>% evaluate(test, testtarget)
pred <- model %>% predict(test)
mean((testtarget-pred)^2)
mean(abs((testtarget-pred)/testtarget)*100)

#prediction chart
plot(testtarget, pred, xlab = "Predicted", ylab = "Actual", cex.lab=2, cex.axis=2, xlim = c(0,250), ylim = c(0,250))
abline(1,1, col="red")

#plot model
n <- neuralnet(Tc ~ .,
               data = data,
               hidden = c(50,50),
               linear.output = F,
               lifesign = 'full',
               rep=1)
plot(n,
     col.hidden = 'darkgreen',
     col.hidden.synapse = 'darkgreen',
     show.weights = F,
     information = F,
     fill = 'lightblue')

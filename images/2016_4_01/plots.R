library(ggplot2)

dat <- data.frame(X=c('Total Number of Papers', 
                      'Plots with error bars', 
                      'Plots with no error bars'),
                  count=c(26, 3, 15))

dat$X <- factor(dat$X, levels=rev(levels(dat$X)))

jpeg('boxplot.jpeg')
ggplot(dat, aes(x=X, y=count)) + 
  geom_bar(stat='identity') + 
  theme_bw() + 
  theme(axis.title.x = element_blank(),
        axis.text.x  = element_text(vjust=0.5, size=14, angle=20),
        axis.title.y = element_text(face="bold", size=16),
        axis.text.y  = element_text(vjust=0.5, size=14)) +
  geom_text(aes(x=X, y=count+1, label=as.character(count)), size=8)
dev.off()


dat <- data.frame(X=rep(c('Group 1', 'Group 2', 'Group 3', 'Group 4'), each=20),
                  Y=c(rnorm(20, mean=5, sd=.5),
                      rnorm(20, mean=6, sd=.5),
                      rnorm(20, mean=5, sd=2),
                      rnorm(20, mean=6, sd=2)))

jpeg('variability.jpeg')
ggplot(dat, aes(x=X, y=Y)) + 
  geom_point(position=position_jitter(width=.25)) +
  theme_bw() + 
  theme(axis.title.x = element_blank(),
        axis.text.x  = element_text(vjust=0.5, size=14),
        axis.title.y = element_text(face="bold", size=16),
        axis.text.y  = element_text(vjust=0.5, size=14)) +
  stat_summary(fun.y=mean, geom='bar', alpha=.25) +
  stat_summary(fun.data=mean_cl_boot, geom='errorbar', width=.2)
dev.off()
